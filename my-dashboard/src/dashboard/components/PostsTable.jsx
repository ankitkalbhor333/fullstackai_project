import React from "react";
import "./poststable.css";

const PostsTable = ({ posts }) => {
  const safePosts = Array.isArray(posts) ? posts : [];

  return (
    <div className="card">
      <h2>📝 Recent Posts ({safePosts.length})</h2>

      {safePosts.length === 0 ? (
        <p style={{ textAlign: "center", color: "#888", padding: "20px" }}>No posts found for this query.</p>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Account</th>
                <th>Text</th>
                <th>Hashtags</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {safePosts.map((p, i) => (
                <tr key={i}>
                  <td><strong>{p.username || p.user_id}</strong></td>
                  <td>{p.content}</td>
                  <td>{Array.isArray(p.hashtags) ? p.hashtags.join(" ") : ""}</td>
                  <td>{p.createdAt ? new Date(p.createdAt).toLocaleString() : "N/A"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default PostsTable;
