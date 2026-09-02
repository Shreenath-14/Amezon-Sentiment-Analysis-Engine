"use client";
import { useState } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

export default function Home() {
  const [url, setUrl] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeReviews = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResults(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/analyze-reviews", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      if (!response.ok) throw new Error(data.error || "Failed to analyze reviews");
      
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container py-5" style={{ maxWidth: "800px" }}>
      {/* Hero Section */}
      <div className="text-center mb-5">
        <i className="bi bi-bar-chart-line-fill text-primary" style={{ fontSize: "3rem" }}></i>
        <h1 className="fw-bold mt-2">Amazon Sentiment Engine</h1>
        <p className="text-muted">Powered by DistilBERT NLP & Flask</p>
      </div>
      
      {/* Input Card */}
      <div className="card border-0 shadow-sm mb-4">
        <div className="card-body p-4">
          <form onSubmit={analyzeReviews}>
            <div className="input-group input-group-lg">
              <span className="input-group-text bg-white text-muted border-end-0">
                <i className="bi bi-link-45deg"></i>
              </span>
              <input
                type="url"
                className="form-control border-start-0 ps-0"
                placeholder="Paste Amazon Product URL..."
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                required
                disabled={loading}
              />
              <button className="btn btn-primary px-4" type="submit" disabled={loading}>
                {loading ? (
                  <><span className="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>Scraping...</>
                ) : (
                  <><i className="bi bi-cpu me-2"></i>Analyze</>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Error State */}
      {error && (
        <div className="alert alert-danger shadow-sm border-0 d-flex align-items-center">
          <i className="bi bi-exclamation-triangle-fill me-3 fs-4"></i>
          <div>{error}</div>
        </div>
      )}

      {/* Results Dashboard */}
      {/* Results Dashboard */}
      {results && (
        <div className="card border-0 shadow-sm bg-transparent">
          
          {/* Top Level Progress Bar */}
          <div className="card border-0 shadow-sm mb-4">
            <div className="card-body p-4">
              <h4 className="fw-bold mb-4 border-bottom pb-3">
                <i className="bi bi-database-check text-success me-2"></i>
                Analysis Overview
              </h4>
              <div className="d-flex justify-content-between mb-1">
                <span className="text-muted fw-semibold">Net Sentiment Score</span>
                <span className="fw-bold">{results.sentiment_summary.average_score?.toFixed(1)} / 100</span>
              </div>
              <div className="progress" style={{ height: "12px" }}>
                <div 
                  className={`progress-bar ${results.sentiment_summary.average_score >= 75 ? 'bg-success' : results.sentiment_summary.average_score >= 40 ? 'bg-warning' : 'bg-danger'}`} 
                  role="progressbar" 
                  style={{ width: `${results.sentiment_summary.average_score}%` }}
                ></div>
              </div>
            </div>
          </div>

          {/* KPI Cards Row */}
          <div className="row g-3 mb-4">
            <div className="col-md-4">
              <div className="card border-0 shadow-sm h-100 p-3 text-center justify-content-center">
                <div className="text-muted small fw-bold text-uppercase mb-2">Total Extracted</div>
                <div className="fs-2 fw-bold text-dark">{results.review_count}</div>
              </div>
            </div>
            
            <div className="col-md-4">
              <div className="card border-0 shadow-sm h-100 p-3 text-center justify-content-center">
                <div className="text-muted small fw-bold text-uppercase mb-2">Sentiment Split</div>
                <div className="d-flex justify-content-center gap-2 mt-1">
                  <span className="badge bg-success-subtle text-success border border-success-subtle fs-6 px-3 py-2">
                    <i className="bi bi-emoji-smile-fill me-2"></i>
                    {results.sentiment_summary.detailed_analysis.filter(r => r.label === 'POSITIVE').length}
                  </span>
                  <span className="badge bg-danger-subtle text-danger border border-danger-subtle fs-6 px-3 py-2">
                    <i className="bi bi-emoji-frown-fill me-2"></i>
                    {results.sentiment_summary.detailed_analysis.filter(r => r.label === 'NEGATIVE').length}
                  </span>
                </div>
              </div>
            </div>

            <div className="col-md-4">
              <div className="card border-0 shadow-sm h-100 p-3 text-center justify-content-center">
                <div className="text-muted small fw-bold text-uppercase mb-2">AI Verdict</div>
                <div>
                  {results.sentiment_summary.average_score >= 75 ? (
                    <span className="badge bg-success fs-5 px-3 py-2"><i className="bi bi-star-fill me-2"></i>Excellent</span>
                  ) : results.sentiment_summary.average_score >= 40 ? (
                    <span className="badge bg-warning text-dark fs-5 px-3 py-2"><i className="bi bi-dash-circle-fill me-2"></i>Mixed</span>
                  ) : (
                    <span className="badge bg-danger fs-5 px-3 py-2"><i className="bi bi-exclamation-octagon-fill me-2"></i>Poor</span>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Granular Data List */}
          <div className="card border-0 shadow-sm">
            <div className="card-body p-4">
              <h6 className="text-muted fw-bold mb-3 text-uppercase">Granular NLP Output</h6>
              <ul className="list-group list-group-flush border-top">
                {results.sentiment_summary.detailed_analysis.map((review, index) => (
                  <li key={index} className="list-group-item px-0 py-3 d-flex justify-content-between align-items-start">
                    <div className="me-4 text-break" style={{ fontSize: "0.95rem" }}>
                      {review.text}
                    </div>
                    <div className="text-end" style={{ minWidth: "120px" }}>
                      <span className={`badge rounded-pill ${review.label === 'POSITIVE' ? 'bg-success-subtle text-success border border-success-subtle' : 'bg-danger-subtle text-danger border border-danger-subtle'} w-100 mb-1`}>
                        {review.label}
                      </span>
                      <div className="text-muted" style={{ fontSize: "0.75rem" }}>
                        Conf: {(review.confidence * 100).toFixed(1)}%
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>

        </div>
      )}
    </div>
  );
}