#!/bin/bash

echo -n "ALVO [+]: "
read alvo 

echo -n "PORTA/PORTAS [+]: "
read ports

echo -n "TIMMING 0-5 [+]: "
read tim

echo " [=] SCANNING DE PORTAS TCP"
sudo nmap -T$tim -sS $alvo -p$ports > scanning_$alvo.txt
echo "___________________________ " >> scanning_$alvo.txt

echo " [=] SCANNING DE PORTAS UDP"
sudo nmap -T$tim -sU $alvo -p$ports >> scanning_$alvo.txt
echo "___________________________ " >> scanning_$alvo.txt

echo " [=] SCANNING DE SERVICOS "
sudo nmap -T$tim -sV $alvo -p$ports >> scanning_$alvo.txt
echo "___________________________ " >> scanning_$alvo.txt

echo " [=] SCANNING DE SISTEMA OPERACIONAL "
sudo nmap -T$tim -sO $alvo -p$ports >> scanning_$alvo.txt
