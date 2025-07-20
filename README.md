# 🌍 VoyageCraft - AI Travel Planner

**Design unforgettable journeys with AI at your side**

VoyageCraft is an intelligent travel planning application that uses AI to create personalized itineraries, budget breakdowns, and travel recommendations. Built with Python Flask backend and vanilla JavaScript frontend, it leverages the power of Groq's LLaMA models to provide comprehensive travel planning assistance.

## ✨ Features

- **🎯 AI-Powered Recommendations**: Get personalized travel suggestions based on your preferences
- **📅 Detailed Itineraries**: Day-by-day plans with activities, timings, and cost estimates
- **💰 Smart Budget Planning**: Comprehensive budget breakdowns in Indian Rupees (₹)
- **🏨 Accommodation Suggestions**: Hotels and stay options for different budgets
- **🚗 Transportation Options**: Complete transport information with costs
- **💡 Local Insights & Tips**: Essential local knowledge and cultural tips
- **👥 Group Travel Support**: Planning for 1-20 travelers
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Live Demo

[Visit VoyageCraft](https://voyagecraft.vercel.app/) 

## 🛠️ Technology Stack

### Backend
- **Python 3.9+**
- **Flask 2.3.3** - Web framework
- **LangChain** - AI model integration
- **Groq** - LLaMA 3.3 70B model for AI responses
- **Pydantic** - Data validation

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with animations
- **Vanilla JavaScript** - Interactive functionality
- **Responsive Design** - Mobile-first approach

### Deployment
- **Vercel** - Serverless deployment platform
- **Environment Variables** - Secure API key management

## 📦 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Groq API key ([Get it here](https://console.groq.com))
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vedpatel2708/voyagecraft.git
   cd voyagecraft
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file in root directory
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
FLASK_ENV=development  # Optional: for development mode
```

### Groq API Setup

1. Visit [Groq Console](https://console.groq.com)
2. Create an account or sign in
3. Generate an API key
4. Add the key to your `.env` file

## 🌐 Deployment

### Vercel Deployment

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy to Vercel**
   ```bash
   vercel --prod
   ```

3. **Set environment variables in Vercel dashboard**
   - Go to your project settings
   - Add `GROQ_API_KEY` in Environment Variables

### Manual Deployment

The project includes a `vercel.json` configuration file for seamless deployment on Vercel platform.

## 📁 Project Structure

```
voyagecraft/
├── app.py                 # Main Flask application
├── travel_planner.py      # AI travel planning logic
├── models.py              # Data models and schemas
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment configuration
├── .env                  # Environment variables (create this)
├── static/
│   ├── style.css         # Styling and animations
│   └── app.js           # Frontend JavaScript logic
├── templates/
│   └── index.html       # Main HTML template
└── README.md            # Project documentation
```

## 🎯 Usage

### Planning a Trip

1. **Enter Destination**: City or country name
2. **Select Duration**: From 1 day to 1 month
3. **Choose Budget**: Budget, Mid-range, or Luxury (in ₹)
4. **Pick Travel Style**: Cultural, Adventure, Relaxation, etc.
5. **Add Interests**: Museums, food, nightlife, shopping, etc.
6. **Set Group Size**: 1-20 travelers
7. **Special Requests**: Optional accessibility or dietary needs
8. **Generate Plan**: Click "Plan My Trip" and wait for AI magic!

### Exploring Results

The AI generates comprehensive travel information across 5 tabs:

- **📅 Itinerary**: Day-by-day activities with timings and costs
- **💰 Budget**: Detailed expense breakdown by category
- **💡 Local Tips**: Cultural insights, safety tips, and local knowledge
- **🚗 Transport**: Airport transfers, local transport, and costs
- **🏨 Hotels**: Accommodation recommendations by area and budget

## 🔍 API Endpoints

```python
POST /plan-trip
```

**Request Body:**
```json
{
  "destination": "Mumbai, India",
  "duration": "3 days",
  "budget": "mid-range",
  "travel_style": "cultural",
  "interests": ["museums", "food", "shopping"],
  "special_requests": "Vegetarian food options",
  "group_size": 2
}
```

**Response:**
```json
{
  "success": true,
  "itinerary": "HTML formatted itinerary",
  "budget": "HTML formatted budget breakdown",
  "tips": "HTML formatted local tips",
  "transportation": "HTML formatted transport info",
  "accommodation": "HTML formatted hotel suggestions"
}
```

## 🎨 Customization

### Styling
- Edit `static/style.css` for visual customizations
- Modify color schemes, fonts, and animations
- Update responsive breakpoints

### AI Prompts
- Customize prompts in `travel_planner.py`
- Adjust response formats and content structure
- Fine-tune AI behavior for different use cases

### Features
- Add new input fields in `index.html`
- Extend JavaScript functionality in `static/app.js`
- Create additional API endpoints in `app.py`

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Use meaningful commit messages
- Test your changes thoroughly
- Update documentation as needed

## 🐛 Troubleshooting

### Common Issues

**Issue: API Key Error**
```
Solution: Ensure GROQ_API_KEY is set in .env file and valid
```

**Issue: Module Import Error**
```
Solution: Activate virtual environment and reinstall requirements
pip install -r requirements.txt
```

**Issue: Vercel Deployment Fails**
```
Solution: Check vercel.json configuration and environment variables
```

### Debug Mode

Enable Flask debug mode for development:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Creator

**Ved Patel**
- 📧 Email: [vedpatel3283@gmail.com](mailto:vedpatel3283@gmail.com)
- 💼 LinkedIn: [Ved Patel](https://www.linkedin.com/in/ved-patel-b65458259)
- 💻 GitHub: [@Vedpatel2708](https://github.com/Vedpatel2708)
- 🌐 Portfolio: [vedpatel2708.github.io/Portfolio](https://vedpatel2708.github.io/Portfolio/)

## 🙏 Acknowledgments

- **Groq** for providing powerful LLaMA model APIs
- **LangChain** for AI model integration framework
- **Flask** team for the excellent web framework
- **Vercel** for seamless deployment platform

## 📈 Project Stats

- **Lines of Code**: 2,000+
- **Languages**: Python, JavaScript, HTML, CSS
- **AI Model**: LLaMA 3.3 70B Versatile
- **Deployment**: Serverless (Vercel)

## 🔮 Future Enhancements

- [ ] User authentication and saved trips
- [ ] Integration with booking APIs
- [ ] Multi-language support
- [ ] Weather integration
- [ ] Social sharing features
- [ ] Mobile app development
- [ ] Premium features with advanced AI models

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/Vedpatel2708/voyagecraft/issues) page
2. Create a new issue with detailed description
3. Contact the creator directly via email

---

**⭐ If you found this project helpful, please give it a star on GitHub!**

*Built with ❤️ by Ved Patel | Powered by AI*
