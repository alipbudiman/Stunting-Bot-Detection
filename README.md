# Stunting Detection Application with Chatbot

## Brief Description

This application is an innovative expert system that combines chatbot technology with the Certainty Factor (CF) method to detect and assess stunting risk in children. The system works by:

1. **Data Collection**: Users input basic child data (height, weight, age, gender)
2. **Interactive Assessment**: Chatbot conducts a structured interview about the child's conditions
3. **Expert Analysis**: System processes data using Certainty Factor algorithms with expert-defined rules
4. **Result Generation**: Provides stunting risk assessment with confidence levels and recommendations

Key Features:
- Secure user authentication via WhatsApp OTP
- Dynamic chatbot conversations based on user responses
- Real-time stunting risk calculation
- Evidence-based recommendations
- Comprehensive history tracking

Target Users:
- Parents/Guardians
- Healthcare Workers
- Child Development Specialists
- Public Health Officials

# Stunting Detection Application with Chatbot

A web-based expert system application that implements the Certainty Factor mechanism to detect stunting in children through an interactive chatbot interface.

## Project Overview

This application is developed as part of the research titled:
"Innovation of Stunting Detection Application Using Chatbot as Strategy to Achieve Universal Health Coverage in SDGs"

The system utilizes an expert system approach with Certainty Factor (CF) mechanism to evaluate stunting risk in children based on various physical and behavioral parameters.

## Features

- User authentication with WhatsApp OTP verification
- Interactive chatbot interface for data collection
- Expert system implementation using Certainty Factor
- Physical measurements analysis (height, weight)
- Behavioral and developmental assessment
- Detailed history tracking of assessments
- Comprehensive stunting risk evaluation
- Professional recommendations based on results

## Technical Requirements

- Python 3.8 or higher
- MongoDB 4.4 or higher
- Flask web framework
- Additional Python packages (see requirements.txt)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### 1. MongoDB Setup
1. Install MongoDB on your system
2. Create a new database
3. Update the MongoDB connection string in `config.py`:
```python
self.MONGDB_URI = "mongodb://username:password@host:port/database"
```

### 2. WhatsApp OTP Configuration
1. Set up a WhatsApp OTP service
2. Update the OTP server address in `config.py`:
```python
self.SERVER_WA_OTP_ADDRESS = "http://your_otp_server:port"
```

### 3. Application Secret
1. Generate a secure random key
2. Update the secret key in `config.py`:
```python
self.APP_SECRET = "your_secure_secret_key"
```

## WhatsApp OTP Integration

### Overview
The application uses WhatsApp OTP (One-Time Password) for user verification. This system ensures secure user registration and authentication through WhatsApp messages.

### OTP Flow
1. User enters registration details
2. System generates a 6-digit OTP
3. OTP is sent to user's WhatsApp number
4. User enters OTP to verify account
5. Account is activated upon successful verification

### OTP Configuration Options

#### 1. Using Provided WhatsApp OTP Service
Contact developer for integration:
- Phone: 082113791904
- Features:
  - Automated WhatsApp message delivery
  - OTP generation and validation
  - Secure message encryption
  - Rate limiting protection
  - Failed attempt monitoring

#### 2. Custom Implementation
Build your own OTP system using:
1. WhatsApp Business API
2. Custom WhatsApp Bot
   - Example implementation: [Go-OpenAI-WhatsApp-Bot](https://github.com/alipbudiman/Go-OpenAI-WhatsApp-Bot)
   - Required modifications:
     ```python
     # Add OTP generation
     # Add message template
     # Implement verification endpoints
     ```

### Security Measures
1. OTP Expiration: 10 minutes
2. Maximum Attempts: 3 tries
3. Cooldown Period: 10 minutes after failed attempts
4. IP-based Rate Limiting
5. Phone Number Validation
6. Anti-Spam Protection

### OTP Server Configuration

## Database Collections

The application uses the following MongoDB collections:

1. `account` - User authentication data
2. `user_log` - Active session data
3. `user_history` - Historical assessment records

## Certainty Factor Implementation

The system evaluates stunting risk using multiple factors:

1. Physical Measurements (G1, G2)
   - Height-for-age ratio
   - Weight-for-height ratio

2. Health Indicators (G3, G4)
   - Cognitive development
   - Infection susceptibility

3. Growth Patterns (G5)
   - Body composition changes
   - Growth velocity

4. Behavioral Indicators (G6-G9)
   - Social interaction
   - Feeding practices
   - Medical history

## Running the Application

Start the application:
```bash
python app.py
```
The application will be available at `http://localhost:5000`

## Security Considerations

1. Always use HTTPS in production
2. Regularly update dependencies
3. Implement rate limiting for OTP requests
4. Use secure session management
5. Validate all user inputs

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## Support

For WhatsApp OTP integration support or questions, contact:
- Developer: 082113791904
- Alternative: Build custom solution using example at [Go-OpenAI-WhatsApp-Bot](https://github.com/alipbudiman/Go-OpenAI-WhatsApp-Bot)

## License

This project is licensed under the MIT License - see the LICENSE file for details.