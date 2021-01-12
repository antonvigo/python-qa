#!/bin/bash

echo '# ====> Lint (error only mode) testing'
echo '######################################################################'
pylint --disable=all --enable=E ../calc2.py
echo -e '\n'

echo '# ====> Unit testing'
echo '######################################################################'
python3 -m unittest unit_tests.py
echo -e '\n'

echo '# ====> Integration testing'
echo '######################################################################'
./integ_testrunner.py
echo -e '\n'

echo '# ====> Smoke testing'
echo '######################################################################'
sudo service calc2app start
sleep 1
echo 'curl to http://unoume-qa12.devops.rebrain.srwx.net status:'
curl -I 'http://unoume-qa12.devops.rebrain.srwx.net'
echo -e '\n'

echo '# ====> API testing'
echo '######################################################################'
#curl -X POST -F "operation=3,+,18" "http://unoume-qa12.devops.rebrain.srwx.net/calc"
./api_testrunner.py
echo -e '\n'

echo '# ====> Interface testing'
echo '######################################################################'
python3 -m unittest iface_tests.py
echo -e '\n'

echo '# ====> Load testing'
echo '######################################################################'
#jmeter -n -t QA12-jM-plan.jmx -l load-test.jtl -e
#cat ./report-output/statistics.json | jq
#rm -rf report-output
#rm -rf temp
#rm load-test.jtl
#rm jmeter.log
echo -e '\n'

echo '# ====> Clean trash'
echo '######################################################################'
sudo service calc2app stop
rm ./calcdb.db
rm -rf __pycache__
