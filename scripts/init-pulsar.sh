#!/bin/bash

# Script para inicializar Pulsar con los topics necesarios para Content Management

echo "Esperando a que Pulsar esté disponible..."
sleep 30

# Crear tenant y namespace
pulsar-admin tenants create content-management || echo "Tenant ya existe"
pulsar-admin namespaces create content-management/events || echo "Namespace ya existe"

# Crear topics para eventos de contenido
pulsar-admin topics create persistent://content-management/events/content-events || echo "Topic content-events ya existe"

echo "Inicialización de Pulsar completada para Content Management"
