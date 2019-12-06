cd ..

echo "====== PULLING LATEST ==========="
git pull -X theirs

echo "======== FIXING PERMS ==========="
chown pi:www-data . -R
