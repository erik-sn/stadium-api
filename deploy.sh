sudo rm -rf static/django
rm -rf static/css
rm -rf static/js
rm -rf static/media
rm scigym/config/templates/config/index.html

cd ../scigym-web
npm run build

cp -r ./build/static/* ../scigym-api/static
cp ./build/index.html ../scigym-api/scigym/config/templates/config/
cp ./build/favicon.png ../scigym-api/static/images/

cd ../scigym-api