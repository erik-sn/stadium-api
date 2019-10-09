sudo rm -rf static/django
rm -rf static/css
rm -rf static/js
rm -rf static/media
rm scigym/config/templates/config/index.html
rm static/precache-manifest.*

AWS_S3_FOLDER="https://scigym.s3.eu-central-1.amazonaws.com/"

cd ../scigym-web # assumes we have api as a sibling of web in directories
npm run build

# create-react-app builds this index html and uses it's relative path from the build
# so we replace all of these static links with the AWS S3 location
# sed -i -e "s,/static/,${AWS_S3_FOLDER},g" build/index.html

cp -r ./build/static/* ../scigym-api/static
cp ./build/index.html ../scigym-api/scigym/config/templates/config/
cp ./build/index.html ../scigym-api/static/
cp ./build/favicon.png ../scigym-api/static/images/
cp ./build/asset-manifest.json ../scigym-api/static/
cp ./build/precache-manifest.* ../scigym-api/static/
cp ./build/service-worker.js ../scigym-api/static/
cp ./build/manifest.json ../scigym-api/static/

cd ../scigym-api
