const express = require("express");
const { PrismaClient } = require("@prisma/client");
const { authMiddleware, roleMiddleware } = require("../middleware/auth");

const router = express.Router();
const prisma = new PrismaClient();

// Search and filter lawyers
router.get("/", async (req, res) => {
  try {
    let {
      specialization,
      availability,
      minExperience,
      page = 1,
      limit = 10,
    } = req.query;

    // Ensure pagination parameters are numbers
    page = Number(page);
    limit = Number(limit);

    if (isNaN(page) || page < 1) page = 1;
    if (isNaN(limit) || limit < 1) limit = 10;

    const where = {
      ...(specialization && { specialization: { has: specialization } }),
      ...(availability !== undefined && {
        availability: availability === "true",
      }),
      ...(minExperience && { yearsExperience: { gte: Number(minExperience) } }),
    };

    const [lawyers, total] = await Promise.all([
      prisma.lawyer.findMany({
        where,
        include: {
          user: {
            select: {
              firstName: true,
              lastName: true,
              email: true,
              phone: true,
            },
          },
        },
        take: limit,
        skip: (page - 1) * limit,
      }),
      prisma.lawyer.count({ where }),
    ]);

    res.json({
      lawyers,
      pagination: {
        currentPage: page,
        totalPages: Math.ceil(total / limit),
        totalLawyers: total,
      },
    });
  } catch (error) {
    console.error("Error fetching lawyers:", error);
    res.status(500).json({ error: "Failed to fetch lawyers" });
  }
});

// Get lawyer profile
router.get(
  "/profile",
  authMiddleware,
  roleMiddleware(["LAWYER"]),
  async (req, res) => {
    try {
      const lawyerProfile = await prisma.lawyer.findUnique({
        where: { userId: req.user.id },
        include: {
          user: {
            select: {
              firstName: true,
              lastName: true,
              email: true,
              phone: true,
            },
          },
          casesHandled: true,
        },
      });

      if (!lawyerProfile)
        return res.status(404).json({ error: "Lawyer profile not found" });

      res.json(lawyerProfile);
    } catch (error) {
      console.error("Error fetching lawyer profile:", error);
      res.status(500).json({ error: "Failed to retrieve lawyer profile" });
    }
  }
);

// Update lawyer profile
router.patch(
  "/profile",
  authMiddleware,
  roleMiddleware(["LAWYER"]),
  async (req, res) => {
    try {
      const { specialization, yearsExperience, barAssociation, availability } =
        req.body;

      const updatedLawyer = await prisma.lawyer.update({
        where: { userId: req.user.id },
        data: {
          ...(specialization && { specialization }),
          ...(yearsExperience && { yearsExperience }),
          ...(barAssociation && { barAssociation }),
          ...(availability !== undefined && { availability }),
        },
      });

      res.json(updatedLawyer);
    } catch (error) {
      console.error("Error updating lawyer profile:", error);
      res.status(500).json({ error: "Failed to update lawyer profile" });
    }
  }
);

// Gracefully close Prisma client when the process exits
process.on("SIGINT", async () => {
  await prisma.$disconnect();
  process.exit();
});

module.exports = router;
