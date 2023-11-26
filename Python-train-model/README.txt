IMPORTANT NOTES!
1.In "outputModels" folder, learned models have following characters: <CNN_utility><shifting><model_version>, where:
- "CNN_utility" is either MediaPipe (S) or OpenPose (O),
- "shifting" is either shift (S) or no shift - original (O),
- "model_version" is integer from 1 to infinity

2. In "outputModels" folder, learned models use following model classes (located in "models" folder):
- HSRecModel_MO1 - UniversalModelV1,
- HSRecModel_MS1 - UniversalModelV1,
- HSRecModel_OO1 - UniversalModelV1,
- HSRecModel_OS1 - UniversalModelV1

This is important, since after providing options "-m" or "-o", "-s" or "-S", "-v", we have also to provide "-n" with model class name parameter.
Otherwise, program will use default parameters also for model class name, which is "UniversalModelV1.py", that may be not appropriate to future learned models.

3. Always provide "-i" option with value of input file name (located inside "input" folder).