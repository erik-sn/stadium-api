rm -rf stadium/config/static/config/css
rm -rf stadium/config/static/config/js
# rm stadium/config/templates/config/index.html

cd ../stadium-web
npm run build

cp -r ./build/static/* ../stadium-api/stadium/config/static/config
cp ./build/index.html ../stadium-api/stadium/config/templates/config/

cd ../stadium-api