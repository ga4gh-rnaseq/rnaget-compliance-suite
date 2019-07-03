#!/bin/bash

set -e # exit with non-zero exit code if anything fails

# only run script if travis branch is master
# and this is NOT a PR
if [[ $TRAVIS_BRANCH == "master" && $TRAVIS_PULL_REQUEST == "false" ]]; then

# run the compliance suite, saving results to the "report" directory
rnaget-compliance report -c user_config_template.yaml -o report

# go to home and set up git
cd $HOME
git config --global user.email "jeremy.adams@ga4gh.org"
git config --global user.name "Jeremy Adams"

#using token clone gh-pages branch
git clone --quiet --branch=gh-pages https://${GH_TOKEN}@github.com/${GH_USER}/${GH_REPO}.git gh-pages > /dev/null

#go into directory and copy data we're interested in to that directory
cd gh-pages
cp -Rf $HOME/ga4gh-rnaseq/rnaget-compliance-suite/report .

#add, commit and push files
git add -f report
git commit -m "Travis build $TRAVIS_BUILD_NUMBER"
git push -fq origin gh-pages > /dev/null

echo "Done updating gh-pages"

else
echo "Skipped updating gh-pages, because build is not triggered from the master branch."
fi;