// routes/cases.js
const express = require('express');
const { PrismaClient } = require('@prisma/client');
const { authMiddleware, roleMiddleware } = require('../middleware/auth');
const multer = require('multer');
const path = require('path');

const router = express.Router();
const prisma = new PrismaClient();

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/evidence/');
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  }
});
const upload = multer({ 
  storage: storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB file size limit
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type. Only JPEG, PNG, and PDF are allowed.'));
    }
  }
});

// Create a new case
router.post('/submit', 
  authMiddleware, 
  roleMiddleware(['CLIENT']),
  upload.array('evidence', 5), // Allow up to 5 evidence files
  async (req, res) => {
    try {
      const { details } = req.body;
      
      // Process uploaded files
      const evidenceFiles = req.files 
        ? req.files.map(file => file.path) 
        : [];

      // Basic validation
      if (!details) {
        return res.status(400).json({ error: 'Case details are required' });
      }

      // Create case in database
      const newCase = await prisma.case.create({
        data: {
          clientId: req.user.id,
          details: details,
          evidenceFiles: evidenceFiles,
          status: 'PENDING'
        }
      });

      res.status(201).json(newCase);
    } catch (error) {
      console.error('Case submission error:', error);
      res.status(500).json({ error: 'Failed to submit case' });
    }
});

// Get user's cases
router.get('/', 
  authMiddleware, 
  async (req, res) => {
    try {
      const cases = await prisma.case.findMany({
        where: { 
          clientId: req.user.id 
        },
        orderBy: { 
          createdAt: 'desc' 
        },
        include: {
          lawyer: {
            select: {
              user: {
                select: {
                  firstName: true,
                  lastName: true
                }
              }
            }
          }
        }
      });

      res.json(cases);
    } catch (error) {
      console.error('Fetch cases error:', error);
      res.status(500).json({ error: 'Failed to retrieve cases' });
    }
});

// Get specific case details
router.get('/:caseId', 
  authMiddleware, 
  async (req, res) => {
    try {
      const caseDetails = await prisma.case.findUnique({
        where: { 
          id: req.params.caseId,
          clientId: req.user.id 
        },
        include: {
          lawyer: {
            include: {
              user: {
                select: {
                  firstName: true,
                  lastName: true,
                  email: true
                }
              }
            }
          }
        }
      });

      if (!caseDetails) {
        return res.status(404).json({ error: 'Case not found' });
      }

      res.json(caseDetails);
    } catch (error) {
      console.error('Case details error:', error);
      res.status(500).json({ error: 'Failed to retrieve case details' });
    }
});

// Update case status (for lawyers)
router.patch('/:caseId/status', 
  authMiddleware, 
  roleMiddleware(['LAWYER', 'ADMIN']),
  async (req, res) => {
    try {
      const { status, legalAdvice } = req.body;

      const updatedCase = await prisma.case.update({
        where: { id: req.params.caseId },
        data: { 
          status,
          legalAdvice,
          lawyerId: req.user.role === 'LAWYER' ? req.user.id : undefined
        }
      });

      res.json(updatedCase);
    } catch (error) {
      console.error('Case update error:', error);
      res.status(500).json({ error: 'Failed to update case' });
    }
});

module.exports = router;