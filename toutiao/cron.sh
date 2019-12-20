#! /bin/sh                                                                                                                                            

export PATH=$PATH:/usr/local/bin

cd /home/lis/Desktop/toutiao/toutiao

nohup scrapy crawl tt >> tt.log 2>&1 &
