 # Cold Email Automations - Frontend

A modern React frontend for the Cold Email Automations project. This application provides a beautiful and intuitive interface for generating personalized cold emails from job postings using AI.

## Features

- 🎨 **Modern UI/UX**: Clean, responsive design built with Tailwind CSS
- 📝 **Email Generation**: Generate cold emails from job URLs or descriptions
- 🔍 **Job Analysis**: AI-powered job posting analysis and skill extraction
- 📊 **Portfolio Matching**: Automatic matching of portfolio projects with job requirements
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- 📋 **Email History**: View and manage previously generated emails
- 💾 **Export Functionality**: Download individual emails or bulk export

## Tech Stack

- **React 18**: Modern React with hooks and functional components
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icon library
- **Axios**: HTTP client for API requests

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend API running on `http://localhost:8000`

### Installation

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

4. **Open your browser** and navigate to `http://localhost:3000`

### Building for Production

```bash
npm run build
```

This creates a `build` folder with optimized production files.

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Header.js
│   │   ├── EmailForm.js
│   │   ├── EmailResults.js
│   │   └── LoadingSpinner.js
│   ├── pages/
│   │   ├── Home.js
│   │   ├── EmailGenerator.js
│   │   └── History.js
│   ├── App.js
│   ├── index.js
│   └── index.css
├── package.json
├── tailwind.config.js
└── postcss.config.js
```

## API Integration

The frontend communicates with the backend API through the following endpoints:

- `POST /generate-emails`: Generate cold emails from job data
- `GET /health`: Health check endpoint

### Request Format

```javascript
// For URL input
{
  "url": "https://example.com/careers/job-posting"
}

// For job description input
{
  "job_description": "We are looking for a Python developer..."
}
```

### Response Format

```javascript
{
  "success": true,
  "message": "Successfully generated 3 emails",
  "emails": [
    {
      "job_title": "Senior Python Developer",
      "job_description": "...",
      "required_skills": ["Python", "Django", "PostgreSQL"],
      "experience_level": "3-5 years",
      "email_content": "Dear Hiring Manager...",
      "portfolio_matches": ["project1.com", "project2.com"],
      "location": "Remote",
      "work_type": "Full-time"
    }
  ],
  "total_jobs": 3
}
```

## Key Components

### EmailForm
Handles user input for job URLs or descriptions with validation and submission.

### EmailResults
Displays generated emails with expandable details, copy functionality, and download options.

### Header
Navigation component with responsive design and active state management.

### LoadingSpinner
Reusable loading component with customizable sizes.

## Styling

The application uses Tailwind CSS for styling with a custom color scheme:

- Primary colors: Blue palette (`primary-50` to `primary-900`)
- Responsive design with mobile-first approach
- Consistent spacing and typography
- Smooth transitions and hover effects

## Development

### Adding New Features

1. Create new components in the `src/components/` directory
2. Add new pages in the `src/pages/` directory
3. Update routing in `App.js` if needed
4. Follow the existing code patterns and styling conventions

### Code Style

- Use functional components with hooks
- Follow React best practices
- Use Tailwind CSS classes for styling
- Maintain consistent naming conventions
- Add proper error handling

## Troubleshooting

### Common Issues

1. **API Connection Error**: Ensure the backend is running on `http://localhost:8000`
2. **Build Errors**: Clear `node_modules` and reinstall dependencies
3. **Styling Issues**: Verify Tailwind CSS is properly configured

### Development Tips

- Use React Developer Tools for debugging
- Check the browser console for API errors
- Test responsive design on different screen sizes
- Validate form inputs before submission

## Contributing

1. Follow the existing code structure and patterns
2. Add proper error handling and loading states
3. Test on multiple devices and browsers
4. Update documentation for new features

## License

This project is licensed under the MIT License.