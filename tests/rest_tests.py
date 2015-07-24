#!/usr/bin/env python

from unittest import TestCase, main
import json

import requests
import psycopg2

connection = psycopg2.connect(user='postgres', database='ag_rest',
                              host='localhost')
cursor = connection.cursor()


class RESTTests(TestCase):
    def test_otu(self):
        resp = requests.get('http://127.0.0.1:8080/sample/')
        obs_full = json.loads(resp.content)
        for sample in obs_full:
            resp = requests.get('http://127.0.0.1:8080/otu/%s' % sample)
            obs = json.loads(resp.content)
            cursor.execute("select biom from biom where sample=%s",
                           [sample])
            exp = cursor.fetchone()[0]
            self.assertEqual(obs, exp)

    def test_sample(self):
        resp = requests.get('http://127.0.0.1:8080/sample/')
        obs_full = json.loads(resp.content)
        self.assertEqual(len(obs_full), 10)
        cursor.execute("select sample from biom")
        exp = {i[0] for i in cursor.fetchall()}
        obs = set(obs_full)
        self.assertEqual(obs, exp)

if __name__ == '__main__':
    main()
