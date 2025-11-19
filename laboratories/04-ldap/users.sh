cat << EOL >> users.ldif
dn: cn=osproxy,ou=system,$BASE
objectClass: organizationalRole
objectClass: simpleSecurityObject
cn: osproxy
userPassword:{SSHA512}CBVaUdQC9mVvAi+0O92J3hA+aPdiWUqf4lVr6bGRAUsFJX5aFOEb+1pSsY8PQwW1UKuuCGO2+160HotnfjXIaRKlryVekLnu
description: OS proxy for resolving UIDs/GIDs

EOL

groups=("programadors" "dissenyadors")
gids=("5000" "5001")
users=("jordi" "manel")
sn=("mateo" "lopez")
uids=("4000" "4001")
programadors=("jordi")
dissenyadors=("manel")

for (( j=0; j<${#groups[@]}; j++ ))
do
cat << EOL >> users.ldif
dn: cn=${groups[$j]},ou=groups,$BASE
objectClass: posixGroup
cn: ${groups[$j]}
gidNumber: ${gids[$j]}

EOL
done

for (( j=0; j<${#users[@]}; j++ ))
do
cat << EOL >> users.ldif
dn: uid=${users[$j]},ou=users,$BASE
objectClass: posixAccount
objectClass: shadowAccount
objectClass: inetOrgPerson
cn: ${users[$j]}
sn: ${sn[$j]}
uidNumber: ${uids[$j]}
gidNumber: ${uids[$j]}
homeDirectory: /home/${users[$j]}
loginShell: /bin/sh

EOL
done