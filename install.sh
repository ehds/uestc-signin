# !/bin/bash
rm -rf driver data logs
mkdir driver data logs

echo "Installing geckodriver"
pushd driver
curl -fSL https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz -o geckodriver.tar.gz
tar -zxvf geckodriver.tar.gz
rm -rf *.gz
popd

pip3 install -r requirments.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
echo "Successfuly installed"
