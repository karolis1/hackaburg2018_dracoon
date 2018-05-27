#!/usr/bin/env bash

KEAFOLDER=/home/justas/git/hackaburg18/kea/kea-5.0_full

cd $KEAFOLDER

export KEAHOME=${KEAFOLDER}
export CLASSPATH=$CLASSPATH:$KEAHOME
export CLASSPATH=$CLASSPATH:$KEAHOME/lib/commons-logging.jar
export CLASSPATH=$CLASSPATH:$KEAHOME/lib/icu4j_3_4.jar
export CLASSPATH=$CLASSPATH:$KEAHOME/lib/iri.jar
export CLASSPATH=$CLASSPATH:$KEAHOME/lib/jena.jar
export CLASSPATH=$CLASSPATH:$KEAHOME/lib/kea-5.0.jar
export CLASSPATH=$CLASSPATH:$KEAHOME/lib/snowball.jar
export CLASSPATH=$CLASSPATH:$KEAHOME/lib/weka.jar
export CLASSPATH=$CLASSPATH:$KEAHOME/lib/xercesImpl.jar

java kea.main.KEAKeyphraseExtractor -l ../../hackaburg2018_dracoon/kea_sets/kea_test_unlabelled -m dracoon_simple  -v none -i de
