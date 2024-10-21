#! /bin/bash

cd ../

mvn dependency:analyze -Djdeps.skip=true > scripts/mvn-unused-declared-deps.log
mvn jdeps:jdkinternals > scripts/jdeps-jdkinternals.log