# Use the official Python image from the Docker Hub as the base image
FROM python:3.13.5-slim-bookworm

# Copy the 'uv' and 'uvx' executables from the latest uv image into /bin/ in this image
# 'uv' is a fast Python package installer and environment manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory inside the container to /code
# All subsequent commands will be run from here
WORKDIR /code

# Add the virtual environment's bin directory to the PATH so Python tools work globally
ENV PATH="/code/.venv/bin:$PATH"

# Copy the project configuration files into the container
# pyproject.toml     → project metadata and dependencies
# uv.lock            → locked dependency versions (for reproducibility)
# .python-version    → Python version specification
COPY "pyproject.toml" "uv.lock" ".python-version" ./

# Install dependencies exactly as locked in uv.lock, without updating them
RUN uv sync --locked

# Copy only the required from src files to the container
COPY src ./src

# Expose TCP port 9696 so it can be accessed from outside the container
EXPOSE 9696

# Run the application using uvicorn (ASGI server)
# src.app:app → refers to 'app' object inside src/app.py file
# --host 0.0.0.0 → listen on all interfaces
# --port 9696    → listen on port 9696
ENTRYPOINT [ "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "9696"]