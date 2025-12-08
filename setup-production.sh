#!/bin/bash

# Production Setup Script for RFM Project
# This script helps initialize the project with proper security configurations

set -e

echo "🔒 RFM Project - Production Setup"
echo "================================="
echo ""

# Check if .env already exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists. Skipping creation."
else
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✓ Created .env"
    echo "⚠️  IMPORTANT: Edit .env with your actual configuration values"
fi

# Check if backend/.env already exists
if [ -f backend/.env ]; then
    echo "⚠️  backend/.env file already exists. Skipping creation."
else
    echo "📝 Creating backend/.env file from template..."
    cp backend/.env.example backend/.env
    echo "✓ Created backend/.env"
    echo "⚠️  IMPORTANT: Edit backend/.env with your actual configuration values"
fi

# Generate database password if db/password.txt doesn't exist
if [ ! -f db/password.txt ]; then
    echo ""
    echo "🔐 Generating secure database password..."
    
    # Check if Python 3 is available
    if command -v python3 &> /dev/null; then
        # Generate a secure password
        DB_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || echo "")
        if [ -n "$DB_PASSWORD" ]; then
            echo "$DB_PASSWORD" > db/password.txt
            chmod 600 db/password.txt
            echo "✓ Generated secure database password"
            echo "  Password saved to: db/password.txt (permissions: 600)"
            echo ""
            echo "📋 Add this password to your .env file:"
            echo "  MYSQL_ROOT_PASSWORD=$DB_PASSWORD"
        fi
    else
        echo "⚠️  Python 3 not found. Please manually create db/password.txt with a secure password."
        echo "  Command: echo 'your_secure_password' > db/password.txt"
    fi
else
    echo "✓ db/password.txt already exists"
fi

# Generate JWT secret if not in .env
if grep -q "JWT_SECRET_KEY=your_secure_random_key_here" .env; then
    echo ""
    echo "🔐 Generating secure JWT secret..."
    
    if command -v python3 &> /dev/null; then
        JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null || echo "")
        if [ -n "$JWT_SECRET" ]; then
            # Update .env file with new JWT secret
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                sed -i '' "s/JWT_SECRET_KEY=your_secure_random_key_here.*/JWT_SECRET_KEY=$JWT_SECRET/" .env
                sed -i '' "s/JWT_SECRET_KEY=your_secure_random_key_here.*/JWT_SECRET_KEY=$JWT_SECRET/" backend/.env
            else
                # Linux
                sed -i "s/JWT_SECRET_KEY=your_secure_random_key_here.*/JWT_SECRET_KEY=$JWT_SECRET/" .env
                sed -i "s/JWT_SECRET_KEY=your_secure_random_key_here.*/JWT_SECRET_KEY=$JWT_SECRET/" backend/.env
            fi
            echo "✓ Generated and updated JWT secret"
        fi
    fi
fi

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Edit .env with your environment-specific values"
echo "2. Edit backend/.env with your backend configuration"
echo "3. Verify db/password.txt contains a secure password"
echo "4. Review SECURITY.md for additional security recommendations"
echo "5. Run: docker-compose config (to validate configuration)"
echo "6. Run: docker-compose up -d (to start services)"
echo ""
echo "🔒 Security Reminders:"
echo "   • Never commit .env or db/password.txt to version control"
echo "   • Keep all secrets in .env files, not in code"
echo "   • Rotate secrets regularly in production"
echo "   • Use strong, unique passwords (32+ characters)"
echo "   • Review SECURITY.md for production hardening steps"
echo ""
