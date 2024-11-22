
# Open Source Report Tool Project Plan

---

## **I. Introduction**

This plan outlines the development of an open-source report tool designed to be flexible, extensible, and user-friendly. The primary goals are to create a robust report engine and output handlers, integrate with various storage solutions, and provide optional features that enhance user experience.

---

## **II. Core Development Tasks**

### **A. Develop the Report Engine Abstract Class**

1. **Implement the `run()` Function**
   - **Priority:** High
   - **Description:** Core function to execute the report generation process.
2. **Define a Report Engine Data Model (Pydantic)**
   - **Priority:** High
   - **Description:** Use Pydantic for data validation and settings management.
3. **Implement a Batch Run Function**
   - **Priority:** Medium
   - **Description:** Allow processing multiple reports in a single run.
4. **Add File Metadata Capabilities**
   - **Priority:** Medium
   - **Description:** Include metadata like author, creation date, and tags.
5. **Design for Handling Any Output File Type**
   - **Priority:** High
   - **Description:** Allow customization to support various file formats.
6. **Allow Users to Set Progress Bars (Optional)**
   - **Priority:** Low
   - **Description:** Enhance user experience during long-running processes.
7. **Implement Status Checks and Run Logs (Optional)**
   - **Priority:** Low
   - **Description:** Provide insights into the report generation status.

### **B. Create Output Handlers**

1. **Develop a Base Abstract Handler**
   - **Priority:** High
   - **Description:** A foundation for all output handlers to extend.
2. **Implement Standard Stream Output**
   - **Priority:** High
   - **Description:** Write PDF bytes to `stdout` for easy redirection.
   - **Example Usage:** `docker run --rm report-tool > report.pdf`
3. **Implement Mounted Volume Support**
   - **Priority:** High
   - **Description:** Allow reading/writing files via host-container volume mapping.
4. **Integrate Blob Storage Support**
   - **Priority:** Medium
   - **Description:** Provide handlers for AWS S3, Azure Blob Storage, etc.

---

## **III. Additional Features and Enhancements**

### **A. Cloud Service Integration**

1. **AWS S3, Azure Blob Storage, Google Cloud Storage**
   - **Priority:** Medium
   - **Description:** Built-in support for common cloud storage platforms.
   - **Implementation:** Use environment variables or config files for credentials.

### **B. Webhook Notifications**

1. **Send Webhook Callbacks Upon Completion**
   - **Priority:** Low
   - **Description:** Notify external services when a report is generated.
   - **Details:** Include URL or file path in the payload.

### **C. Chained Outputs**

1. **Combine Multiple Output Handlers**
   - **Priority:** Low
   - **Description:** Enable saving locally and uploading to the cloud simultaneously.

---

## **IV. Docker Integration and Usage**

### **A. Command Examples**

1. **Generate Report with Local Output**
   ```bash
   docker run --rm report-tool generate --output-type local --filename /data/report.pdf
   ```
2. **Generate Report and Write to Stdout**
   ```bash
   docker run --rm report-tool generate --output-type stdout > report.pdf
   ```
3. **Generate Report and Upload to S3**
   ```bash
   docker run --rm report-tool generate --output-type s3 --filename report.pdf
   ```

### **B. Mounted Volume for Local Output**

1. **Understanding Volume Mapping**
   - **Host Directory:** Your local machine's directory (e.g., `$(pwd)`).
   - **Container Directory:** Directory inside the container (e.g., `/data`).
2. **Example Command with Volume Mapping**
   ```bash
   docker run --rm -v $(pwd):/data report-tool generate --output-type local --filename /data/report.pdf
   ```
   - **Explanation:**
     - `-v $(pwd):/data`: Maps current directory to `/data` in the container.
     - `--filename /data/report.pdf`: Saves output to the mapped directory.
3. **Graceful Warnings**
   - **Priority:** High
   - **Description:** Detect when no volume is mounted and warn the user.
   - **Benefit:** Prevents confusion when output files do not persist.

---

## **V. Prioritization and Implementation Plan**

### **Phase 1: Core Development (High Priority)**

1. **Develop Report Engine Abstract Class**
   - Implement `run()` function.
   - Define data model with Pydantic.
   - Design for multiple output file types.
2. **Create Output Handlers**
   - Develop base abstract handler.
   - Implement standard stream output and mounted volume support.
3. **Docker Integration**
   - Ensure seamless execution via Docker.
   - Implement graceful warnings for missing volume mounts.

### **Phase 2: Enhancements (Medium Priority)**

1. **Batch Run Functionality**
2. **File Metadata Capabilities**
3. **Blob Storage Integration**
   - Begin with the most commonly used services.
4. **Progress Bars and Status Logs (Optional)**

### **Phase 3: Advanced Features (Low Priority)**

1. **Cloud Service Integration**
   - Extend blob storage support to additional platforms.
2. **Webhook Notifications**
   - Implement callback system post-report generation.
3. **Chained Outputs**
   - Enable combining multiple output handlers.

---

## **VI. Additional Considerations**

### **A. Documentation and User Guidance**

- **Priority:** High
- **Description:** Provide clear documentation, usage examples, and tutorials.

### **B. Error Handling and User Feedback**

- **Implement Clear Error Messages**
- **Provide Solutions or Next Steps in Warnings**

### **C. Extensibility and Customization**

- **Plugin Architecture**
  - Allow users to add custom output handlers.
- **Configuration File Support**
  - Enable default settings and easier management.

### **D. Logging and Monitoring**

- **Implement Logging with Verbosity Levels**
  - Users can select the level of detail in logs.

