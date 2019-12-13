cd ..

echo "====== PULLING LATEST ==========="
git pull --no-edit origin master

echo "======== FIXING PERMS ==========="
chown pi:www-data . -R

echo "======== Restarting API ==========="
systemctl --user restart matcha