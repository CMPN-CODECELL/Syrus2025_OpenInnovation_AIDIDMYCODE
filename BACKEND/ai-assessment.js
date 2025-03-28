// routes/ai-assessment.js
const express = require("express");
const { PrismaClient } = require("@prisma/client");
const { authMiddleware } = require("../middleware/auth");
const axios = require("axios");

const router = express.Router();
const prisma = new PrismaClient();

// AI Case Assessment Endpoint
router.post("/assess-case", authMiddleware, async (req, res) => {
  try {
    const { caseDetails } = req.body;

    // Validate input
    if (!caseDetails) {
      return res.status(400).json({ error: "Case details are required" });
    }

    // Call external AI assessment service (placeholder)
    const aiAssessmentResponse = await axios.post(
      process.env.AI_ASSESSMENT_SERVICE_URL,
      { details: caseDetails },
      {
        headers: {
          Authorization: `Bearer ${process.env.AI_SERVICE_API_KEY}`,
        },
      }
    );

    // Extract assessment score and insights
    const { confidenceScore, potentialFalseAccusation, insights } =
      aiAssessmentResponse.data;

    // Update case with AI assessment
    const updatedCase = await prisma.case.update({
      where: { id: req.body.caseId },
      data: {
        aiAssessmentScore: confidenceScore,
        legalAdvice: insights,
      },
    });

    res.json({
      confidenceScore,
      potentialFalseAccusation,
      insights,
      updatedCase,
    });
  } catch (error) {
    console.error("AI Assessment error:", error);
    res.status(500).json({
      error: "Failed to perform AI assessment",
      details: error.message,
    });
  }
});

module.exports = router;
