#!/bin/bash

set -e # exit with non-zero exit code if anything fails

# only run script if travis branch is master
# and this is NOT a PR
if [[ $TRAVIS_BRANCH == "master" && $TRAVIS_PULL_REQUEST == "false" && $TRAVIS_PYTHON_VERSION == "3.7" ]]; then

# takes the reference implementation yaml file, and replaces placeholder tokens
# with the real token stored in secured travis settings 
CONFIG=`cat config_ref_implementations.yaml`
for TOKEN_VAR in `compgen -A variable | grep ^SERVER_API_KEY`; do
  REPLACE_FROM="$TOKEN_VAR"
  REPLACE_TO="${!TOKEN_VAR}"
  CONFIG=`echo -e "${CONFIG}" | sed -e "s/${REPLACE_FROM}/${REPLACE_TO}/"`
done
echo -e "$CONFIG" > config.yaml

# run the compliance suite, saving results to the "report" directory
# then remove the config file with api tokens
rnaget-compliance report -c config.yaml -o report
rm config.yaml

# go to home and set up git
cd $HOME
git config --global user.email "jeremy.adams@ga4gh.org"
git config --global user.name "Jeremy Adams"

#using token clone gh-pages branch
git clone --quiet --branch=gh-pages https://${GH_TOKEN}@github.com/${GH_USER}/${GH_REPO}.git gh-pages > /dev/null

#go into directory and copy data we're interested in to that directory
cd gh-pages
cp -Rf $HOME/build/ga4gh-rnaseq/rnaget-compliance-suite/report .

#add, commit and push files
git add -f report
git commit -m "Travis build $TRAVIS_BUILD_NUMBER"
git push -fq origin gh-pages > /dev/null

echo "Done updating gh-pages"

else
echo "Skipped updating gh-pages, because build is not triggered from the master branch."
fi;