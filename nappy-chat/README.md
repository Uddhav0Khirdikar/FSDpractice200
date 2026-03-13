# 💬 Nappy Chat - Full Stack Real-Time Chat Application

![Node.js](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)
![Express.js](https://img.shields.io/badge/Express.js-404D59?style=for-the-badge)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![Socket.io](https://img.shields.io/badge/Socket.io-black?style=for-the-badge&logo=socket.io&badgeColor=010101)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)

A modern, responsive real-time chat application built with the MERN stack, featuring instant messaging, user authentication, profile management, and file uploads. This project demonstrates advanced full-stack development skills with real-time communication capabilities.

## 🌐 **Live Demo**
**Experience the application:** [https://fullstack-realtime-chat-app-nappy-chat.onrender.com/login](https://fullstack-realtime-chat-app-nappy-chat.onrender.com/login)

---

## 📋 **Table of Contents**
- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Architecture & Design Patterns](#-architecture--design-patterns)
- [Backend Implementation](#-backend-implementation)
- [Frontend Implementation](#-frontend-implementation)
- [Real-Time Communication](#-real-time-communication)
- [Database Design](#-database-design)
- [Security Implementation](#-security-implementation)
- [File Upload System](#-file-upload-system)
- [Deployment Strategy](#-deployment-strategy)
- [Learning Outcomes](#-learning-outcomes)
- [Installation & Setup](#-installation--setup)
- [API Documentation](#-api-documentation)
- [Future Enhancements](#-future-enhancements)

---

## 🎯 **Project Overview**

Nappy Chat is a sophisticated full-stack real-time messaging application that enables users to communicate instantly with a modern, intuitive interface. The application showcases advanced web development concepts including WebSocket communication, JWT authentication, cloud-based file storage, and responsive design principles.

### **Core Objectives Achieved:**
- **Real-Time Communication**: Implemented bidirectional communication using Socket.IO
- **Secure Authentication**: JWT-based authentication with HTTP-only cookies
- **Modern UI/UX**: Responsive design with smooth user interactions
- **Scalable Architecture**: Modular backend structure with separation of concerns
- **Cloud Integration**: Cloudinary integration for media management
- **Production Deployment**: Successfully deployed on Render with optimized build process

---

## ✨ **Key Features**

### **Authentication System**
- **User Registration & Login**: Secure signup/signin with input validation
- **JWT Token Management**: HTTP-only cookies for enhanced security
- **Protected Routes**: Client and server-side route protection
- **Profile Management**: Users can update profiles with image uploads

### **Real-Time Messaging**
- **Instant Message Delivery**: Real-time bidirectional communication
- **Online Status Tracking**: Live user presence indicators
- **Message History**: Persistent chat history with MongoDB storage
- **Typing Indicators**: Real-time typing status updates

### **User Experience**
- **Responsive Design**: Mobile-first approach with cross-device compatibility
- **Profile Image Upload**: Cloudinary-powered image management
- **User Discovery**: Browse and connect with other users
- **Message Status**: Delivery and read receipts

---

## 🛠 **Technology Stack**

### **Frontend Technologies**
```json
{
  "framework": "React 18.3.1",
  "buildTool": "Vite 6.0.1",
  "language": "JavaScript ES6+",
  "styling": "TailwindCSS and DaisyUI with modern features",
  "httpClient": "Axios for API communication",
  "stateManagement": "React Context API + Hooks",
  "routing": "React Router DOM",
  "realTime": "Socket.IO Client"
}
```

### **Backend Technologies**
```json
{
  "runtime": "Node.js with ES Modules",
  "framework": "Express.js 4.18.2",
  "database": "MongoDB with Mongoose ODM",
  "authentication": "JWT + bcryptjs",
  "realTime": "Socket.IO Server",
  "fileUpload": "Multer + Cloudinary",
  "security": "CORS, Cookie Parser"
}
```

---

## 🏗 **Architecture & Design Patterns**

### **Backend Architecture**
```
backend/
├── src/
│   ├── controllers/     # Business logic layer
│   ├── middleware/      # Authentication & validation
│   ├── models/         # MongoDB schemas
│   ├── routes/         # API route definitions
│   ├── lib/            # Database & Socket configuration
│   └── index.js        # Application entry point
```

### **Design Patterns Implemented**
1. **MVC (Model-View-Controller)**: Clean separation of concerns
2. **Middleware Pattern**: Reusable authentication and validation logic
3. **Factory Pattern**: Database connection and configuration
4. **Observer Pattern**: Real-time event handling with Socket.IO

---

## 🔧 **Backend Implementation**

### **Core Dependencies Analysis**

#### **Express.js Framework**
```javascript
// Primary web application framework
import express from "express";
```
- **Purpose**: Creates RESTful API endpoints and handles HTTP requests
- **Implementation**: Modular route handling with middleware integration
- **Benefits**: Minimal, flexible, and highly performant

#### **Database Layer - MongoDB & Mongoose**
```javascript
import mongoose from "mongoose";
```
- **Purpose**: Object Document Mapper (ODM) for MongoDB
- **Features**: Schema validation, middleware hooks, query building
- **Connection**: Async connection handling with error management

#### **Authentication System**
```javascript
import bcryptjs from "bcryptjs";      // Password hashing
import jsonwebtoken from "jsonwebtoken"; // JWT token generation
import cookieParser from "cookie-parser"; // Cookie management
```
- **Security Flow**: Password hashing → JWT generation → HTTP-only cookies
- **Protection**: Route-level middleware for authenticated endpoints

#### **Real-Time Communication**
```javascript
import { Server } from "socket.io";
```
- **WebSocket Management**: Bidirectional event-based communication
- **Connection Handling**: User presence tracking and message broadcasting
- **Event System**: Custom events for typing, messages, and user status

#### **File Upload System**
```javascript
import multer from "multer";      // Multipart form data handling
import { v2 as cloudinary } from "cloudinary"; // Cloud storage
import streamifier from "streamifier"; // Buffer to stream conversion
```
- **Upload Pipeline**: Memory storage → Stream conversion → Cloudinary upload
- **Optimization**: Automatic image processing and CDN delivery

#### **Security & CORS**
```javascript
import cors from "cors";
```
- **Cross-Origin Requests**: Configured for frontend-backend communication
- **Credentials Support**: Cookie-based authentication across origins

### **Server Configuration**
```javascript
// Integrated HTTP server with Socket.IO
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: process.env.CLIENT_URL,
    credentials: true
  }
});
```

---

## ⚛️ **Frontend Implementation**

### **Core Dependencies Analysis**

#### **React 18.3.1**
- **Modern Features**: Concurrent rendering, automatic batching
- **Hooks Usage**: useState, useEffect, useContext for state management
- **Component Architecture**: Functional components with custom hooks

#### **Vite 6.0.1**
- **Development Server**: Hot Module Replacement (HMR)
- **Build Optimization**: Tree shaking, code splitting
- **Modern JavaScript**: ES modules, TypeScript support

#### **HTTP Communication**
```javascript
import axios from "axios";
```
- **API Integration**: Centralized HTTP client with interceptors
- **Error Handling**: Global error management and response processing
- **Authentication**: Automatic cookie inclusion for authenticated requests

#### **Real-Time Client**
```javascript
import { io } from "socket.io-client";
```
- **WebSocket Client**: Maintains persistent connection with server
- **Event Handling**: Real-time message reception and user status updates

### **State Management Strategy**
- **Context API**: Global authentication and user state
- **Local State**: Component-specific state with useState
- **Effect Hooks**: Side effects and lifecycle management

---

## 🔄 **Real-Time Communication**

### **Socket.IO Implementation**

#### **Server-Side Event Handling**
```javascript
io.on("connection", (socket) => {
  // User connection tracking
  socket.on("user_connected", (userId) => {
    // Update online status
    // Broadcast to other users
  });
  
  // Message broadcasting
  socket.on("send_message", (messageData) => {
    // Save to database
    // Emit to recipient
  });
  
  // Typing indicators
  socket.on("typing", (data) => {
    socket.broadcast.emit("user_typing", data);
  });
});
```

#### **Client-Side Integration**
- **Connection Management**: Automatic reconnection on network issues
- **Event Listeners**: Message reception, typing indicators, user status
- **State Synchronization**: Real-time UI updates based on socket events

### **Communication Flow**
1. **User Authentication**: JWT verification for socket connection
2. **Room Management**: Users join conversation-specific rooms
3. **Message Delivery**: Instant delivery with delivery confirmation
4. **Presence System**: Real-time online/offline status updates

---

## 🗄 **Database Design**

### **MongoDB Schema Architecture**

#### **User Model**
```javascript
const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  fullName: { type: String, required: true },
  password: { type: String, required: true, minlength: 6 },
  profilePic: { type: String, default: "" }
}, { timestamps: true });
```

#### **Message Model**
```javascript
const messageSchema = new mongoose.Schema({
  senderId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
  receiverId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
  text: { type: String },
  image: { type: String }
}, { timestamps: true });
```

### **Database Relationships**
- **One-to-Many**: Users to Messages relationship
- **Population**: Automatic user data population in message queries
- **Indexing**: Optimized queries with compound indexes

---

## 🔐 **Security Implementation**

### **Authentication Flow**
1. **Password Hashing**: bcryptjs with salt rounds for secure storage
2. **JWT Generation**: Signed tokens with user payload and expiration
3. **HTTP-Only Cookies**: Secure token storage preventing XSS attacks
4. **Route Protection**: Middleware verification on protected endpoints

### **Security Middleware**
```javascript
const protectRoute = async (req, res, next) => {
  const token = req.cookies.jwt;
  if (!token) return res.status(401).json({ message: "Unauthorized" });
  
  const decoded = jwt.verify(token, process.env.JWT_SECRET);
  const user = await User.findById(decoded.userId).select("-password");
  req.user = user;
  next();
};
```

### **CORS Configuration**
- **Origin Control**: Restricted to frontend domain
- **Credentials**: Enabled for cookie-based authentication
- **Methods**: Specific HTTP methods allowed

---

## 📁 **File Upload System**

### **Multer Configuration**
```javascript
const upload = multer({ 
  storage: multer.memoryStorage(),
  limits: { fileSize: 5 * 1024 * 1024 } // 5MB limit
});
```

### **Cloudinary Integration**
```javascript
cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET
});
```

### **Upload Pipeline**
1. **Frontend**: File selection and form submission
2. **Multer**: Memory storage and size validation
3. **Stream Conversion**: Buffer to readable stream
4. **Cloudinary**: Upload with automatic optimization
5. **Database**: Store secure URL reference

---

## 🚀 **Deployment Strategy**

### **Render Platform Deployment**

#### **Build Process**
```json
{
  "scripts": {
    "build": "npm install --prefix backend && npm install --prefix frontend && npm run build --prefix frontend",
    "start": "npm run start --prefix backend"
  }
}
```

#### **Environment Configuration**
- **Production Variables**: Database URLs, JWT secrets, API keys
- **CORS Settings**: Dynamic origin configuration for production
- **Static File Serving**: Express serving React build files

#### **Deployment Architecture**
1. **Frontend Build**: Vite builds optimized production bundle
2. **Backend Preparation**: Dependencies installation and configuration
3. **Static File Serving**: Express serves frontend from backend
4. **Database Connection**: MongoDB Atlas integration
5. **Environment Variables**: Secure configuration management

---

## 📚 **Learning Outcomes**

### **Technical Skills Developed**

#### **Full-Stack Development**
- **MERN Stack Mastery**: Complete understanding of MongoDB, Express, React, Node.js
- **API Design**: RESTful API architecture with proper HTTP methods
- **Database Management**: Schema design, relationships, and optimization

#### **Real-Time Programming**
- **WebSocket Implementation**: Bidirectional communication with Socket.IO
- **Event-Driven Architecture**: Real-time event handling and broadcasting
- **Connection Management**: Handling connections, disconnections, and reconnections

#### **Security Best Practices**
- **Authentication Systems**: JWT implementation with secure cookie storage
- **Password Security**: Proper hashing and salting techniques
- **CORS Configuration**: Cross-origin security implementation

#### **Modern Development Tools**
- **Vite Build System**: Fast development and optimized production builds
- **ES6+ Features**: Modern JavaScript with modules and async/await
- **Development Workflow**: Hot reloading, debugging, and testing

#### **Cloud Services Integration**
- **File Upload Handling**: Multipart form data processing
- **Cloud Storage**: Cloudinary integration for media management
- **CDN Utilization**: Optimized content delivery

#### **DevOps & Deployment**
- **Production Deployment**: Full-stack application deployment on Render
- **Environment Management**: Production vs development configurations
- **Build Optimization**: Static file serving and performance optimization

### **Soft Skills Enhanced**
- **Problem Solving**: Debugging complex full-stack issues
- **Architecture Planning**: System design and component organization
- **Code Organization**: Modular, maintainable, and scalable code structure
- **Documentation**: Technical documentation and code commenting

---

## 🛠 **Installation & Setup**

### **Prerequisites**
- Node.js (v14 or higher)
- MongoDB (local or Atlas)
- Cloudinary account for image uploads

### **Local Development Setup**

#### **1. Clone Repository**
```bash
git clone <repository-url>
cd nappy-chat
```

#### **2. Backend Setup**
```bash
cd backend
npm install

# Create .env file
echo "MONGODB_URI=your_mongodb_connection_string" >> .env
echo "JWT_SECRET=your_jwt_secret" >> .env
echo "NODE_ENV=development" >> .env
echo "CLOUDINARY_CLOUD_NAME=your_cloudinary_name" >> .env
echo "CLOUDINARY_API_KEY=your_api_key" >> .env
echo "CLOUDINARY_API_SECRET=your_api_secret" >> .env
echo "PORT=5001" >> .env
```

#### **3. Frontend Setup**
```bash
cd frontend
npm install

# Create .env file with environment variables
echo "VITE_API_URL=http://localhost:5001" >> .env
```

**Frontend Dependencies Installed:**
- **React 19.1.0**: Latest React framework with concurrent features
- **Vite 7.0.4**: Next-generation build tool for faster development
- **Zustand 5.0.7**: Lightweight state management solution
- **Tailwind CSS 3.4.17 + DaisyUI 4.12.23**: Modern styling framework
- **React Router DOM 7.7.1**: Client-side routing
- **Socket.IO Client 4.8.1**: Real-time communication
- **Axios 1.11.0**: HTTP client for API requests
- **Lucide React 0.536.0**: Modern icon library
- **React Hot Toast 2.5.2**: Toast notification system

#### **4. Run Application**
```bash
# Backend (from backend directory)
npm run dev

# Frontend (from frontend directory) 
npm run dev
```

### **Production Build**
```bash
# From root directory
npm run build
npm start
```

---

## 📖 **API Documentation**

### **Authentication Endpoints**

#### **POST /api/auth/signup**
```json
{
  "fullName": "John Doe",
  "email": "john@example.com",
  "password": "securePassword123"
}
```

#### **POST /api/auth/login**
```json
{
  "email": "john@example.com",
  "password": "securePassword123"
}
```

#### **GET /api/auth/me**
- **Headers**: Cookie with JWT token
- **Response**: Current user information

#### **PUT /api/auth/update-profile**
- **Content-Type**: multipart/form-data
- **Fields**: profilePic (file), fullName (text)

#### **POST /api/auth/logout**
- **Action**: Clears JWT cookie

### **Message Endpoints**

#### **GET /api/messages/users**
- **Purpose**: Get all users for chat list
- **Authentication**: Required

#### **GET /api/messages/:userId**
- **Purpose**: Get message history with specific user
- **Authentication**: Required

#### **POST /api/messages/send/:receiverId**
```json
{
  "text": "Hello, how are you?",
  "image": "optional_image_url"
}
```

### **Socket Events**

#### **Client → Server**
- `user_connected`: User comes online
- `send_message`: Send new message
- `typing_start`: User starts typing
- `typing_stop`: User stops typing

#### **Server → Client**
- `message_received`: New message notification
- `user_status_change`: User online/offline status
- `typing_indicator`: Show typing indicator

---

## 🔮 **Future Enhancements**

### **Feature Roadmap**
- [ ] **Group Chat Functionality**: Multi-user conversation rooms
- [ ] **Message Encryption**: End-to-end encryption for enhanced security
- [ ] **Voice Messages**: Audio message recording and playback
- [ ] **File Sharing**: Document and media file sharing capabilities
- [ ] **Message Search**: Full-text search across chat history
- [ ] **Push Notifications**: Browser and mobile push notifications
- [ ] **Theme Customization**: Light/dark mode and custom themes
- [ ] **Message Reactions**: Emoji reactions to messages
- [ ] **Read Receipts**: Message read status indicators
- [ ] **User Blocking**: Block/unblock user functionality

### **Technical Improvements**
- [ ] **TypeScript Migration**: Type safety across the entire application
- [ ] **Unit Testing**: Comprehensive test coverage with Jest
- [ ] **Performance Optimization**: Code splitting and lazy loading
- [ ] **Mobile App**: React Native mobile application
- [ ] **Microservices**: Service-oriented architecture
- [ ] **Redis Integration**: Caching and session management
- [ ] **Docker Containerization**: Containerized deployment
- [ ] **CI/CD Pipeline**: Automated testing and deployment

---

## 🎯 **Conclusion**

Nappy Chat represents a comprehensive demonstration of modern full-stack web development skills, showcasing the ability to build, secure, and deploy real-time applications. The project successfully integrates multiple complex technologies into a cohesive, user-friendly platform while maintaining clean code architecture and security best practices.

This application serves as a testament to proficiency in the MERN stack, real-time programming, cloud services integration, and production deployment strategies. The modular architecture and extensive documentation demonstrate professional-level development practices suitable for enterprise-scale applications.

---

**🔗 Experience the Application:** [https://fullstack-realtime-chat-app-nappy-chat.onrender.com/login](https://fullstack-realtime-chat-app-nappy-chat.onrender.com/login)

---

*Built with ❤️ using modern web technologies*
