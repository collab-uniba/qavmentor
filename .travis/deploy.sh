#!/bin/bash

eval "$(ssh-agent -s)" # Start ssh-agent cache
chmod 600 .travis/id_rsa # Allow read access to the private key
ssh-add .travis/id_rsa # Add the private key to SSH

git config --global push.default matching
echo ____________________remote add deploy____________________
git remote add deploy ssh://root@$IP:$PORT$DEPLOY_DIR
echo ____________________deploying____________________
if [ -z `ssh-keygen -F $IP` ]; then
  ssh-keyscan -H $IP >> ~/.ssh/known_hosts
  echo ____________________public key not recognized, adding to known host____________________
fi
git fetch --unshallow || true
git push deploy master

# Skip this command if you don't need to execute any additional commands after deploying.
ssh root@$IP -p $PORT <<EOF
service apache2 restart
#  cd $DEPLOY_DIR
 # crystal build --release --no-debug index.cr # Change to whatever commands you need!
