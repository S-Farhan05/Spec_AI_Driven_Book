# Data Model: ROS 2 Module

## Entities

### ROS 2 Module
- **Name**: String (e.g., "The Robotic Nervous System")
- **Description**: String (educational content package explaining ROS 2)
- **Chapters**: Array of Chapter entities
- **PracticeSection**: PracticeSection entity
- **TargetAudience**: String (e.g., "CS/AI students and developers new to robotics")
- **WordCount**: Integer (target 1,300-2,000 per chapter)
- **Sources**: Array of Source entities (minimum 20 total, 40% peer-reviewed)

### Chapter
- **Title**: String (chapter title)
- **Content**: String (Markdown content)
- **LearningObjectives**: Array of String (what students will learn)
- **AcceptanceScenarios**: Array of String (criteria for success)
- **Sources**: Array of Source entities
- **Position**: Integer (chapter number 1-6)
- **RelatedConcepts**: Array of String (related topics)

### PracticeSection
- **Title**: String (practice section title)
- **Exercises**: Array of Exercise entities
- **Workflows**: Array of String (small ROS 2 workflow examples)
- **LearningGoals**: Array of String (what practice reinforces)

### Exercise
- **Title**: String (exercise title)
- **Description**: String (what the exercise covers)
- **Difficulty**: Enum (Beginner, Intermediate, Advanced)
- **Instructions**: String (step-by-step instructions)
- **ExpectedOutcome**: String (what student should achieve)
- **Solution**: String (reference solution)

### Source
- **Title**: String (source title)
- **Author**: String (author name)
- **Publication**: String (journal/book/publisher)
- **Date**: Date (publication date)
- **Type**: Enum (Academic, Technical Documentation, Tutorial, Other)
- **Url**: String (source URL if available)
- **Citation**: String (APA format citation)
- **VerificationStatus**: Enum (Verified, Pending, Questionable)

### StudentLearningPath
- **Prerequisites**: Array of String (what students should know)
- **LearningStages**: Array of LearningStage entities
- **SuccessMetrics**: Array of SuccessMetric entities

### LearningStage
- **StageName**: String (name of learning stage)
- **RequiredKnowledge**: Array of String (knowledge needed)
- **Activities**: Array of String (learning activities)
- **AssessmentCriteria**: Array of String (how to assess)

### SuccessMetric
- **MetricName**: String (name of metric)
- **Target**: Number (target percentage/number)
- **MeasurementMethod**: String (how to measure)
- **SuccessThreshold**: Number (minimum acceptable value)

## Relationships

- ROS 2 Module contains 6 Chapter entities
- ROS 2 Module contains 1 PracticeSection entity
- Chapter contains multiple Source entities
- PracticeSection contains multiple Exercise entities
- Exercise may reference multiple Chapter entities
- StudentLearningPath connects to multiple Chapter entities
- Chapter contains multiple LearningStage entities
- LearningStage has multiple SuccessMetric entities

## Validation Rules

- Each Chapter MUST have between 1,300-2,000 words
- Each Chapter MUST include at least 3 Source entities
- At least 40% of all Source entities MUST be Academic type
- Each Chapter MUST have at least 2 AcceptanceScenarios
- PracticeSection MUST include at least 5 Exercise entities
- Each Exercise MUST have a defined Difficulty level
- Each Source MUST have a valid APA format citation
- ROS 2 Module total word count SHOULD be appropriate for 8,000-12,000 book target