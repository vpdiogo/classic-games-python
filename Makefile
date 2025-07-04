.PHONY: help build test clean check format snake pong tetris
.DEFAULT_GOAL := help

# Colors for pretty output
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
NC := \033[0m

help: ## Show this help message
	@echo "$(BLUE)Classic Games Python Collection$(NC)"
	@echo "$(BLUE)==============================$(NC)"
	@echo ""
	@echo "$(GREEN)Global Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -v "^snake\|^pong\|^tetris" | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(BLUE)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Game-Specific Commands:$(NC)"
	@grep -E '^(snake|pong|tetris):.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(BLUE)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Examples:$(NC)"
	@echo "  make build        # Build all games"
	@echo "  make test         # Test all games"
	@echo "  make snake        # Work with Snake game"
	@echo "  make clean        # Clean all builds"

# Global commands that work on all games
build: ## Build all games
	@echo "$(GREEN)🏗️ Building all games...$(NC)"
	@./scripts/build-all.sh build

test: ## Test all games
	@echo "$(GREEN)🧪 Testing all games...$(NC)"
	@./scripts/build-all.sh test

clean: ## Clean all game builds
	@echo "$(GREEN)🧹 Cleaning all games...$(NC)"
	@./scripts/build-all.sh clean

check: ## Run quality checks for all games
	@echo "$(GREEN)🔍 Checking all games...$(NC)"
	@./scripts/build-all.sh check

format: ## Format code for all games
	@echo "$(GREEN)🎨 Formatting all games...$(NC)"
	@for game in snake pong tetris; do \
		if [ -d "$$game" ]; then \
			echo "$(BLUE)Formatting $$game...$(NC)"; \
			cd $$game && make format 2>/dev/null || echo "$(YELLOW)No format target in $$game$(NC)"; \
			cd ..; \
		fi; \
	done

# Individual game shortcuts
snake: ## Enter Snake game directory and show help
	@echo "$(GREEN)🐍 Snake Game Commands:$(NC)"
	@echo "Change to snake directory and run 'make help' for full options"
	@echo ""
	@echo "$(YELLOW)Quick commands (run from root):$(NC)"
	@echo "  cd snake && make dev-setup    # Setup development"
	@echo "  cd snake && make test         # Run tests"
	@echo "  cd snake && make build        # Build package"
	@echo "  cd snake && make run          # Play the game"

pong: ## Pong game (coming soon)
	@echo "$(YELLOW)🏓 Pong Game - Coming Soon!$(NC)"
	@echo "This game is planned for future development."

tetris: ## Tetris game (coming soon)
	@echo "$(YELLOW)🧱 Tetris Game - Coming Soon!$(NC)"
	@echo "This game is planned for future development."

# Development helpers
dev-setup: ## Setup development environment for all games
	@echo "$(GREEN)🚀 Setting up development environment...$(NC)"
	@for game in snake; do \
		if [ -d "$$game" ]; then \
			echo "$(BLUE)Setting up $$game...$(NC)"; \
			cd $$game && make dev-setup 2>/dev/null || echo "$(YELLOW)No dev-setup target in $$game$(NC)"; \
			cd ..; \
		fi; \
	done

# Git helpers
git-status: ## Show git status
	@git status

git-clean-check: ## Check if git working directory is clean
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "$(RED)❌ Working directory is not clean$(NC)"; \
		git status --short; \
		exit 1; \
	else \
		echo "$(GREEN)✅ Working directory is clean$(NC)"; \
	fi

# Release management
release-snake: ## Release Snake game
	@echo "$(GREEN)🚀 Releasing Snake game...$(NC)"
	@cd snake && make release

tag-snake: ## Tag Snake game version
	@echo "$(GREEN)🏷️ Tagging Snake game...$(NC)"
	@cd snake && make tag-and-push

# Information
info: ## Show repository information
	@echo "$(BLUE)Classic Games Python Repository Information$(NC)"
	@echo "$(BLUE)===========================================$(NC)"
	@echo "$(GREEN)Repository:$(NC) Classic Games Python Collection"
	@echo "$(GREEN)Structure:$(NC) Monorepo with independent game packages"
	@echo "$(GREEN)Games:$(NC)"
	@for game in snake pong tetris; do \
		if [ -d "$$game" ]; then \
			echo "  ✅ $$game/ (available)"; \
		else \
			echo "  🚧 $$game/ (planned)"; \
		fi; \
	done
	@echo "$(GREEN)CI/CD:$(NC) GitHub Actions with smart game detection"
	@echo "$(GREEN)Releases:$(NC) Independent per-game releases"

# CI simulation
ci: ## Simulate CI pipeline locally
	@echo "$(GREEN)🤖 Simulating CI pipeline...$(NC)"
	@make git-clean-check
	@make check
	@make test
	@make build
	@echo "$(GREEN)✅ CI simulation completed!$(NC)"

# Docker support (future)
docker: ## Docker support (coming soon)
	@echo "$(YELLOW)🐳 Docker support is planned for future releases$(NC)"

# Documentation
docs: ## Open documentation
	@echo "$(GREEN)📚 Opening documentation...$(NC)"
	@echo "Main README: $(BLUE)$(PWD)/README.md$(NC)"
	@echo "Snake docs: $(BLUE)$(PWD)/snake/README.md$(NC)"
	@if command -v xdg-open >/dev/null 2>&1; then \
		xdg-open README.md; \
	elif command -v open >/dev/null 2>&1; then \
		open README.md; \
	else \
		echo "$(YELLOW)Open README.md manually to view documentation$(NC)"; \
	fi
