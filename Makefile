PG_HOME = /tmp/pg-local
VENV = $(CURDIR)/venv
BACKEND_DIR = $(CURDIR)/backend
FRONTEND_DIR = $(CURDIR)/frontend
PG_PORT = 5555
BACKEND_PORT = 8000
FRONTEND_PORT = 5173

.PHONY: run-pg stop-pg run-backend stop-backend run-frontend stop-frontend run stop

run-pg:
	@echo "Starting PostgreSQL on port $(PG_PORT)..."
	@mkdir -p $(PG_HOME)/data
	@if [ ! -f $(PG_HOME)/data/PG_VERSION ]; then \
		LD_LIBRARY_PATH="$(PG_HOME)/usr/lib:$$LD_LIBRARY_PATH" \
		PATH="$(PG_HOME)/usr/bin:$$PATH" \
		$(PG_HOME)/usr/bin/initdb -D $(PG_HOME)/data --username=reysoft_asistencia --encoding=UTF8 --locale=C 2>/dev/null; \
		echo "unix_socket_directories = '/tmp'" >> $(PG_HOME)/data/postgresql.conf; \
		echo "port = $(PG_PORT)" >> $(PG_HOME)/data/postgresql.conf; \
	fi
	@LD_LIBRARY_PATH="$(PG_HOME)/usr/lib:$$LD_LIBRARY_PATH" \
		PATH="$(PG_HOME)/usr/bin:$$PATH" \
		$(PG_HOME)/usr/bin/pg_ctl -D $(PG_HOME)/data -l /tmp/pg-local/pg.log start 2>/dev/null || true
	@sleep 2
	@LD_LIBRARY_PATH="$(PG_HOME)/usr/lib:$$LD_LIBRARY_PATH" \
		PATH="$(PG_HOME)/usr/bin:$$PATH" \
		$(PG_HOME)/usr/bin/pg_isready -h localhost -p $(PG_PORT) 2>/dev/null
	@echo "PostgreSQL ready."

stop-pg:
	@echo "Stopping PostgreSQL..."
	@LD_LIBRARY_PATH="$(PG_HOME)/usr/lib:$$LD_LIBRARY_PATH" \
		PATH="$(PG_HOME)/usr/bin:$$PATH" \
		$(PG_HOME)/usr/bin/pg_ctl -D $(PG_HOME)/data stop 2>/dev/null || true

run-backend:
	@echo "Starting backend on port $(BACKEND_PORT)..."
	@cd $(BACKEND_DIR) && \
		LD_LIBRARY_PATH="$(PG_HOME)/usr/lib:$$LD_LIBRARY_PATH" \
		PATH="$(PG_HOME)/usr/bin:$$PATH" \
		$(VENV)/bin/uvicorn app.main:app --host 0.0.0.0 --port $(BACKEND_PORT)

stop-backend:
	@kill $$(lsof -ti :$(BACKEND_PORT)) 2>/dev/null || true

run-frontend:
	@echo "Starting frontend on port $(FRONTEND_PORT)..."
	@cd $(FRONTEND_DIR) && npm run dev

stop-frontend:
	@kill $$(lsof -ti :$(FRONTEND_PORT)) 2>/dev/null || true

run: run-pg run-backend

stop: stop-backend stop-frontend stop-pg
	@echo "All services stopped."
