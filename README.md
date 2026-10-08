
cat > README.md << 'EOF'
# 🛡️ Admin Finder - V3 Threaded

Scanner educacional para encontrar painéis administrativos expostos. Para estudos Red Team com autorização.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Purpose](https://img.shields.io/badge/Purpose-Educational-green)

### Resultado Real
Testado em `http://demo.testfire.net` (site vulnerável da IBM) - 11 rotas encontradas:
- /admin [200]
- /admin/login [200]
- /administrator [302]

### Como usar (apenas com autorização)
```bash
pip install requests
python admin_finder.py http://seu-alvo-autorizado.com
