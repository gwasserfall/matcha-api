cd ..

echo "====== PULLING LATEST ==========="
git pull origin master --rebase

echo "======== FIXING PERMS ==========="
chown pi:www-data . -R
