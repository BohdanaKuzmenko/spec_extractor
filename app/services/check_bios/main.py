#!/usr/bin/python
# -*- coding: utf-8 -*

import multiprocessing
from pandas import concat, Series, set_option
from app.services.check_bios.text_normalizer import sentences_splitter
import numpy as np
import os, signal, sys, subprocess


class Extractor(object):
    def __init__(self, regexes):
        self.regexes = regexes

    def get_ai_results(self, bios):
        set_option('display.max_colwidth', -1)
        p = multiprocessing.Pool(4)
        pool_results = p.map(self.filter_with_regex, np.array_split(bios, 4))
        signal.signal(signal.SIGTERM, self.kill_child_processes)
        p.close()
        p.join()
        concatenated = concat(pool_results)
        urls = list(set(concatenated["profileUrl"].values.tolist()))
        result = bios[bios["profileUrl"].isin(urls)]
        result['profileUrl'] = result['profileUrl'].apply(lambda x: '<a href="{}">{}</a>'.format(x, x))
        result['attorneyBio'] = result['attorneyBio'].apply(lambda x: '<p class = "test">{}</p>'.format(x))
        return result

    def kill_child_processes(self, signum, frame):
        parent_id = os.getpid()
        ps_command = subprocess.Popen("ps -o pid --ppid %d --noheaders" % parent_id, shell=True, stdout=subprocess.PIPE)
        ps_output = ps_command.stdout.read()
        retcode = ps_command.wait()
        for pid_str in ps_output.strip().split("\n")[:-1]:
            os.kill(int(pid_str), signal.SIGTERM)
        sys.exit()

    def filter_with_regex(self, bio_df):
        splitted_bios = concat([Series(row['profileUrl'], sentences_splitter(row['attorneyBio']))
                                for _, row in bio_df.iterrows()]).reset_index()

        splitted_bios.columns = ["attorneyBio", "profileUrl"]
        result = []
        for regex in self.regexes:
            print(regex)
            tmp_df = splitted_bios
            result.append(tmp_df[tmp_df['attorneyBio'].str.contains(regex)])
        return concat(result)


if __name__ == "__main__":
    pass
