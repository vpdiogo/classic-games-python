# Development Workflow Guide

Este documento descreve o workflow completo de desenvolvimento para o Snake Game.

## 🔄 Ciclo de Desenvolvimento

### 1. Setup Inicial
```bash
# Clone e configure o ambiente
git clone <repo>
cd snake
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instale dependências de desenvolvimento
pip install -e .[dev]
```

### 2. Desenvolvimento Diário
```bash
# Antes de começar a trabalhar
git pull origin main
git checkout -b feature/nova-funcionalidade

# Durante o desenvolvimento
python run_snake.py          # Testar rapidamente
pytest tests/                # Rodar testes
pytest tests/ -v             # Testes verbosos
pytest tests/ --cov=snake_game  # Com cobertura

# Verificar qualidade do código
black snake_game/             # Formatar código
flake8 snake_game/            # Linting
mypy snake_game/              # Type checking
```

### 3. Antes de Commit
```bash
# Checklist obrigatório
./scripts/check.sh

# Ou manualmente:
pytest tests/                 # ✅ Todos os testes passando
black --check snake_game/     # ✅ Código formatado
flake8 snake_game/            # ✅ Sem warnings de linting
mypy snake_game/              # ✅ Types corretos
```

### 4. Versionamento e Release
```bash
# Para incrementar versão
bumpversion build             # 0.1.0-alpha.1 → 0.1.0-alpha.2
bumpversion minor             # 0.1.0-alpha.1 → 0.2.0-alpha.1
bumpversion release           # 0.1.0-alpha.1 → 0.1.0-beta.1

# Para fazer release
./scripts/release.sh          # Build completo + verificações
```

## 🛠️ Scripts de Automação

### `scripts/setup-dev.sh` - Setup do ambiente
### `scripts/test.sh` - Suite completa de testes  
### `scripts/check.sh` - Verificações de qualidade
### `scripts/build.sh` - Build do pacote
### `scripts/release.sh` - Release completo

## 📋 Checklists

### Antes de cada Commit
- [ ] Testes passando (`pytest`)
- [ ] Código formatado (`black`)
- [ ] Linting limpo (`flake8`)
- [ ] Types corretos (`mypy`)
- [ ] Funcionalidade testada manualmente

### Antes de cada Release
- [ ] Todos os testes passando
- [ ] Versão incrementada (`bumpversion`)
- [ ] CHANGELOG.md atualizado
- [ ] Build funcionando (`./scripts/build.sh`)
- [ ] Executáveis testados
- [ ] Documentação atualizada

## 🏗️ Estrutura de Build

### Build Local
```bash
# Build rápido para teste
python -m build

# Build completo com executáveis
./scripts/build.sh

# Apenas executáveis
pyinstaller snake_game.spec
```

### Verificação de Build
```bash
# Testar pacote wheel
pip install dist/*.whl
snake-game

# Testar executável
./dist/SnakeGame

# Testar código fonte
pip install -e .
```

## 📦 Distribuição

### PyPI (Futuro)
```bash
# Test PyPI primeiro
twine upload --repository testpypi dist/*

# PyPI produção
twine upload dist/*
```

### GitHub Releases
```bash
# Criar tag e push
git tag v0.1.0-alpha.1
git push origin v0.1.0-alpha.1

# GitHub Actions fará o resto
```

## 🚀 Comandos Rápidos (Makefile)

```bash
make install    # Setup desenvolvimento
make test       # Rodar testes
make lint       # Verificar código
make format     # Formatar código
make build      # Build completo
make clean      # Limpar arquivos
make release    # Release completo
```

## 📊 Métricas de Qualidade

### Cobertura de Testes
- **Meta**: >90% de cobertura
- **Comando**: `pytest --cov=snake_game --cov-report=html`

### Qualidade de Código
- **Black**: Formatação automática
- **Flake8**: Linting e style guide
- **MyPy**: Verificação de tipos
- **Pre-commit**: Hooks automáticos

## 🐛 Debugging

### Logs
```bash
# Logs em tempo real
tail -f logs/snake_game.log

# Logs com mais detalhes
export SNAKE_LOG_LEVEL=DEBUG
python run_snake.py
```

### Profiling
```bash
# Performance profiling
python -m cProfile -o profile.stats run_snake.py
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('tottime').print_stats(10)"
```

## 📚 Recursos Úteis

- [Python Packaging Guide](https://packaging.python.org/)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
