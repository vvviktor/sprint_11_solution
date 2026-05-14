#!/bin/bash

# Путь к JSON‑файлу (первый аргумент)
json_file="$1"

# Проверяем существование файла
if [[ ! -f "$json_file" ]]; then
  echo "Ошибка: файл '$json_file' не найден!" >&2
  exit 1
fi

# Читаем JSON из файла
json=$(cat "$json_file")

# Получаем все ключи
keys=$(echo "$json" | jq -r 'keys[]')

# Создаём ассоциативный массив
declare -A vm_dict

for key in $keys; do
  value=$(echo "$json" | jq -r --arg k "$key" '.[$k]')
  vm_dict["$key"]="$value"
done

cat > inventory.yaml << EOF
all:
  hosts:
EOF

counter=1
for vm in "${!vm_dict[@]}"; do
  cat >> inventory.yaml << EOF
    $vm:
      ansible_host: ${vm_dict[$vm]}
      ansible_user: ubuntu
      ansible_ssh_private_key_file: "path/to/key.pem"
EOF
  ((counter++))
done
