#!/bin/bash

# Generic Database Framework - Podman Database Startup Script
# This script helps you start database containers for local development

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if podman is installed
check_podman() {
    if ! command -v podman &> /dev/null; then
        print_error "Podman is not installed. Please install it first."
        echo ""
        echo "Installation instructions:"
        echo "  macOS:   brew install podman"
        echo "  Linux:   sudo apt-get install podman (Debian/Ubuntu)"
        echo "           sudo dnf install podman (Fedora/RHEL)"
        echo "  Windows: Download from https://podman.io/getting-started/installation"
        exit 1
    fi
    print_success "Podman is installed"
}

# Function to check if podman-compose is installed
check_podman_compose() {
    if ! command -v podman-compose &> /dev/null; then
        print_warning "podman-compose is not installed. Attempting to install..."
        pip install podman-compose
        if [ $? -eq 0 ]; then
            print_success "podman-compose installed successfully"
        else
            print_error "Failed to install podman-compose. Please install it manually:"
            echo "  pip install podman-compose"
            exit 1
        fi
    else
        print_success "podman-compose is installed"
    fi
}

# Function to start all databases
start_all() {
    print_info "Starting all database containers..."
    podman-compose up -d
    print_success "All databases started successfully!"
    show_connection_info
}

# Function to start specific database
start_specific() {
    local db=$1
    print_info "Starting $db container..."
    podman-compose up -d $db
    print_success "$db started successfully!"
}

# Function to stop all databases
stop_all() {
    print_info "Stopping all database containers..."
    podman-compose down
    print_success "All databases stopped successfully!"
}

# Function to stop specific database
stop_specific() {
    local db=$1
    print_info "Stopping $db container..."
    podman-compose stop $db
    print_success "$db stopped successfully!"
}

# Function to show status
show_status() {
    print_info "Database container status:"
    podman-compose ps
}

# Function to show logs
show_logs() {
    local db=$1
    if [ -z "$db" ]; then
        print_info "Showing logs for all databases..."
        podman-compose logs -f
    else
        print_info "Showing logs for $db..."
        podman-compose logs -f $db
    fi
}

# Function to restart databases
restart_all() {
    print_info "Restarting all database containers..."
    podman-compose restart
    print_success "All databases restarted successfully!"
}

# Function to restart specific database
restart_specific() {
    local db=$1
    print_info "Restarting $db container..."
    podman-compose restart $db
    print_success "$db restarted successfully!"
}

# Function to clean up (remove containers and volumes)
cleanup() {
    print_warning "This will remove all containers and volumes. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_info "Cleaning up containers and volumes..."
        podman-compose down -v
        print_success "Cleanup completed!"
    else
        print_info "Cleanup cancelled"
    fi
}

# Function to show connection information
show_connection_info() {
    echo ""
    print_info "Database Connection Information:"
    echo ""
    echo "MySQL:"
    echo "  Host: localhost"
    echo "  Port: 3306"
    echo "  User: testuser"
    echo "  Password: testpassword"
    echo "  Database: testdb"
    echo ""
    echo "PostgreSQL:"
    echo "  Host: localhost"
    echo "  Port: 5432"
    echo "  User: testuser"
    echo "  Password: testpassword"
    echo "  Database: testdb"
    echo ""
    echo "MongoDB:"
    echo "  Host: localhost"
    echo "  Port: 27017"
    echo "  User: testuser"
    echo "  Password: testpassword"
    echo "  Database: testdb"
    echo ""
    echo "Redis:"
    echo "  Host: localhost"
    echo "  Port: 6379"
    echo "  Password: testpassword"
    echo ""
    echo "Elasticsearch:"
    echo "  Host: localhost"
    echo "  Port: 9200"
    echo "  No authentication"
    echo ""
    echo "Cassandra:"
    echo "  Host: localhost"
    echo "  Port: 9042"
    echo ""
    echo "Neo4j:"
    echo "  HTTP: http://localhost:7474"
    echo "  Bolt: bolt://localhost:7687"
    echo "  User: neo4j"
    echo "  Password: testpassword"
    echo ""
    echo "InfluxDB:"
    echo "  Host: localhost"
    echo "  Port: 8086"
    echo "  User: testuser"
    echo "  Password: testpassword"
    echo "  Org: testorg"
    echo "  Bucket: testbucket"
    echo "  Token: test-token-please-change-in-production"
    echo ""
    echo "MariaDB:"
    echo "  Host: localhost"
    echo "  Port: 3307"
    echo "  User: testuser"
    echo "  Password: testpassword"
    echo "  Database: testdb"
    echo ""
    echo "CouchDB:"
    echo "  Host: localhost"
    echo "  Port: 5984"
    echo "  User: testuser"
    echo "  Password: testpassword"
    echo ""
    echo "Milvus:"
    echo "  Host: localhost"
    echo "  Port: 19530"
    echo ""
}

# Function to show help
show_help() {
    echo "Generic Database Framework - Podman Database Management"
    echo ""
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  start [db]       Start all databases or specific database"
    echo "  stop [db]        Stop all databases or specific database"
    echo "  restart [db]     Restart all databases or specific database"
    echo "  status           Show status of all database containers"
    echo "  logs [db]        Show logs for all or specific database"
    echo "  info             Show connection information"
    echo "  cleanup          Remove all containers and volumes"
    echo "  help             Show this help message"
    echo ""
    echo "Available databases:"
    echo "  mysql, postgresql, mongodb, redis, elasticsearch,"
    echo "  cassandra, neo4j, influxdb, mariadb, couchdb, milvus-standalone"
    echo ""
    echo "Examples:"
    echo "  $0 start                    # Start all databases"
    echo "  $0 start mysql              # Start only MySQL"
    echo "  $0 stop                     # Stop all databases"
    echo "  $0 logs mysql               # Show MySQL logs"
    echo "  $0 status                   # Show container status"
    echo "  $0 info                     # Show connection info"
    echo ""
}

# Main script logic
main() {
    # Check prerequisites
    check_podman
    check_podman_compose

    # Parse command
    case "${1:-help}" in
        start)
            if [ -z "$2" ]; then
                start_all
            else
                start_specific "$2"
            fi
            ;;
        stop)
            if [ -z "$2" ]; then
                stop_all
            else
                stop_specific "$2"
            fi
            ;;
        restart)
            if [ -z "$2" ]; then
                restart_all
            else
                restart_specific "$2"
            fi
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs "$2"
            ;;
        info)
            show_connection_info
            ;;
        cleanup)
            cleanup
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"

# Made with Bob
