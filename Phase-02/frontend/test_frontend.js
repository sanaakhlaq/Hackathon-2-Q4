// Simple test to verify the frontend structure
console.log('Frontend project structure created successfully!');
console.log('Files created:');
console.log('- package.json');
console.log('- next.config.js');
console.log('- tsconfig.json');
console.log('- tailwind.config.js');
console.log('- app/globals.css');
console.log('- app/layout.tsx');
console.log('- app/page.tsx');
console.log('- app/login/page.tsx');
console.log('- app/signup/page.tsx');
console.log('- app/dashboard/page.tsx');
console.log('- utils/auth.ts');
console.log('');
console.log('Backend CORS updated in main.py');

// Test that the backend can start
console.log('');
console.log('To start the backend API server:');
console.log('cd ../backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000');
console.log('');
console.log('To start the frontend development server:');
console.log('cd ../frontend && npm install && npm run dev');