
####################################################################################
selenium_lib_path=./layers/selenium-binaries
python_dep_path=./layers/python-dependencies
mkdir -p layers layers/selenium-binaries 
mkdir -p layers/python-dependencies
mkdir -p ${python_dep_path}/python/lib/python3.6/site-packages



pip install -r requirements.txt -t ${python_dep_path}/python/lib/python3.6/site-packages


zip -r ../python-dependencies.zip .


####################################################################################
zip -r ../selenium-binaries.zip .

function download_chromedriver_and_headless_chromium() 
{
    # remove previous driver and binary (empty folder selenium-binaries)
    rm -r -f $selenium_lib_path/

    # create folder if not present
    mkdir -p $selenium_lib_path/
    
    # download and unzip driver and binary
    curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > $selenium_lib_path/chromedriver.zip
    unzip $selenium_lib_path/chromedriver.zip -d $selenium_lib_path/
    rm $selenium_lib_path/chromedriver.zip
    
    curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-41/stable-headless-chromium-amazonlinux-2017-03.zip > $selenium_lib_path/headless-chromium.zip
    unzip $selenium_lib_path/headless-chromium.zip -d $selenium_lib_path/
    rm $selenium_lib_path/headless-chromium.zip
}
