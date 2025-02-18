import React, { useState } from "react";

const ProfileSubmission = () => {
  const [formData, setFormData] = useState({
    name: "",
    phone: "",
    projects: "",
    education: "",
    image: null,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleImageChange = (e) => {
    setFormData((prev) => ({ ...prev, image: e.target.files[0] }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Submitted Data:", formData);
  };

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column", backgroundColor: "#f3f4f6" }}>
      <header style={{ backgroundColor: "#4f46e5", color: "#fff", textAlign: "center", padding: "16px", fontSize: "24px", fontWeight: "600" }}>
        Profile Submission
      </header>
      <main style={{ flex: 1, display: "flex", justifyContent: "center", alignItems: "center", padding: "16px" }}>
        <form
          style={{
            backgroundColor: "#fff",
            boxShadow: "0px 4px 10px rgba(0,0,0,0.1)",
            borderRadius: "10px",
            padding: "20px",
            width: "100%",
            maxWidth: "500px",
          }}
          onSubmit={handleSubmit}
        >
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#374151", marginBottom: "20px", textAlign: "center" }}>Fill out the details</h2>

          <div style={{ marginBottom: "15px" }}>
            <label style={{ display: "block", color: "#374151", marginBottom: "5px" }}>Name:</label>
            <input
              type="text"
              name="name"
              style={{
                width: "100%",
                border: "1px solid #d1d5db",
                padding: "10px",
                borderRadius: "5px",
                outline: "none",
              }}
              onChange={handleChange}
              required
            />
          </div>

          <div style={{ marginBottom: "15px" }}>
            <label style={{ display: "block", color: "#374151", marginBottom: "5px" }}>Phone Number:</label>
            <input
              type="text"
              name="phone"
              style={{
                width: "100%",
                border: "1px solid #d1d5db",
                padding: "10px",
                borderRadius: "5px",
                outline: "none",
              }}
              onChange={handleChange}
              required
            />
          </div>

          <div style={{ marginBottom: "15px" }}>
            <label style={{ display: "block", color: "#374151", marginBottom: "5px" }}>Projects:</label>
            <textarea
              name="projects"
              style={{
                width: "100%",
                border: "1px solid #d1d5db",
                padding: "10px",
                borderRadius: "5px",
                outline: "none",
                resize: "vertical",
              }}
              onChange={handleChange}
              required
            ></textarea>
          </div>

          <div style={{ marginBottom: "15px" }}>
            <label style={{ display: "block", color: "#374151", marginBottom: "5px" }}>Educational Background:</label>
            <textarea
              name="education"
              style={{
                width: "100%",
                border: "1px solid #d1d5db",
                padding: "10px",
                borderRadius: "5px",
                outline: "none",
                resize: "vertical",
              }}
              onChange={handleChange}
              required
            ></textarea>
          </div>

          <div style={{ marginBottom: "20px" }}>
            <label style={{ display: "block", color: "#374151", marginBottom: "5px" }}>Profile Picture:</label>
            <input
              type="file"
              accept="image/*"
              style={{
                width: "100%",
                border: "1px solid #d1d5db",
                padding: "10px",
                borderRadius: "5px",
                outline: "none",
              }}
              onChange={handleImageChange}
            />
          </div>

          <button
            type="submit"
            style={{
              width: "100%",
              padding: "12px",
              backgroundColor: "#4f46e5",
              color: "#fff",
              fontSize: "16px",
              fontWeight: "600",
              borderRadius: "5px",
              border: "none",
              cursor: "pointer",
            }}
          >
            Submit
          </button>
        </form>
      </main>
      <footer style={{ backgroundColor: "#1f2937", color: "#fff", textAlign: "center", padding: "12px", fontSize: "14px" }}>
        &copy; 2025 Profile Submission. All rights reserved.
      </footer>
    </div>
  );
};

export default ProfileSubmission;
