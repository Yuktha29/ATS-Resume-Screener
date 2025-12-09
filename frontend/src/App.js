import React, { useState } from 'react';
import { Upload, FileText, Bot, CheckCircle, AlertCircle, Loader } from 'lucide-react';


const App = () => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [feedback, setFeedback] = useState(null);

  const handleAnalyze = () => {
  if (!uploadedFile) {
    alert("Please upload a resume first.");
    return;
  }
  setIsProcessing(true);
  const formData = new FormData();
  formData.append('resume', uploadedFile);
  formData.append('jobDesc', jobDescription || '');
  
  fetch('http://localhost:5001/analyze', {
    method: 'POST',
    body: formData,
  })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        alert('Error: ' + data.error);
      } else {
        setFeedback(data);
      }
      setIsProcessing(false);
    })
    .catch(err => {
      console.error(err);
      alert('Failed to analyze resume. Is backend running on port 5001?');
      setIsProcessing(false);
    });
};

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setUploadedFile(file);
      setIsProcessing(true);
      uploadToBackend(file);
    }
  };

  const handleDragOver = (e) => e.preventDefault();

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
      setUploadedFile(file);
      setIsProcessing(true);
      uploadToBackend(file);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <h1 className="text-xl font-semibold text-gray-900">ResumeAI Feedback</h1>
            </div>
            <div className="text-sm text-gray-500">
              Get instant AI-powered resume analysis
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
         {/* Left Panel - Input Section */}
<div className="lg:col-span-1">
  <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
    <div className="flex items-center space-x-2 mb-4">
      <Upload className="w-5 h-5 text-indigo-600" />
      <h2 className="text-lg font-semibold text-gray-900">Resume & Job Description</h2>
    </div>

    {/* Job Description - Always Visible */}
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Job Description (optional)
      </label>
      <textarea
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
        placeholder="Paste job description here..."
        className="w-full text-sm border border-gray-300 rounded p-2 h-24 resize-none"
      />
    </div>

    {/* Resume Upload */}
    {!uploadedFile ? (
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
        <FileText className="w-10 h-10 text-gray-400 mx-auto mb-3" />
        <p className="text-sm text-gray-700">Upload your resume (PDF only)</p>
        <label className="mt-2 inline-block px-4 py-2 bg-indigo-600 text-white text-sm rounded-lg cursor-pointer hover:bg-indigo-700">
          Choose File
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => e.target.files[0] && setUploadedFile(e.target.files[0])}
            className="hidden"
          />
        </label>
      </div>
    ) : (
      <div className="space-y-3">
        <div className="flex items-center space-x-2 p-2 bg-gray-50 rounded">
          <FileText className="w-4 h-4 text-indigo-600" />
          <span className="text-sm truncate">{uploadedFile.name}</span>
        </div>
      </div>
    )}

    {/* Analyze Button */}
    <button
      onClick={handleAnalyze}
      disabled={!uploadedFile || isProcessing}
      className={`w-full mt-4 py-2 text-sm font-medium rounded-lg ${
        !uploadedFile || isProcessing
          ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
          : 'bg-indigo-600 text-white hover:bg-indigo-700'
      }`}
    >
      {isProcessing ? 'Analyzing...' : 'Analyze Resume'}
    </button>

    {/* Reset Button */}
    {feedback && (
      <button
        onClick={() => {
          setUploadedFile(null);
          setJobDescription('');
          setFeedback(null);
        }}
        className="w-full mt-2 text-sm text-gray-600 hover:text-gray-800"
      >
        Upload Different Resume
      </button>
    )}
  </div>
</div>

         {/* Center Panel - PDF Preview */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Resume Preview</h2>
            </div>
            <div className="h-96 bg-gray-100 flex items-center justify-center">
              {uploadedFile ? (
                <div className="text-center">
                  <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600 text-sm">Uploaded: {uploadedFile.name}</p>
                  <p className="text-xs text-gray-500 mt-1">Preview not rendered (text only)</p>
                </div>
              ) : (
                <div className="text-center">
                  <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">Upload a PDF to preview</p>
                </div>
              )}
            </div>
          </div>
        </div>

          {/* Right Panel - AI Feedback */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200">
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center space-x-2">
                  <Bot className="w-5 h-5 text-indigo-600" />
                  <h2 className="text-lg font-semibold text-gray-900">AI Feedback</h2>
                </div>
              </div>

              {!feedback ? (
                <div className="p-6 text-center">
                  <Bot className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">Upload a resume to get AI feedback</p>
                </div>
              ) : (
                <div className="p-6 space-y-6">
                  {/* Overall Score */}
                  <div className="bg-indigo-50 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-indigo-800">Overall Score</span>
                      <span className="text-lg font-bold text-indigo-600">{feedback.overallScore}/100</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-indigo-600 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${feedback.overallScore}%` }}
                      ></div>
                    </div>
                  </div>

                <div className="mt-4">
                  <h3 className="font-medium text-gray-900">Predicted Resume Category</h3>
                  <p className="text-sm text-gray-600">{feedback.predictedCategory}</p>
                </div>

                  {/* Summary */}
                  <div>
                    <h3 className="font-medium text-gray-900 mb-2">Analysis Summary</h3>
                    <p className="text-sm text-gray-600 leading-relaxed">{feedback.summary}</p>
                  </div>

                  {/* Category Feedback */}
                  <div className="space-y-4">
                    {feedback.categories.map((category, index) => (
                      <div key={index} className="border border-gray-200 rounded-lg p-4">
                        <div className="flex items-center justify-between mb-3">
                          <h4 className="font-medium text-gray-900">{category.title}</h4>
                          <span className="text-sm font-medium text-indigo-600">
                            {category.score}/100
                          </span>
                        </div>
                        <div className="space-y-2">
                          {category.issues.map((issue, issueIndex) => (
                            <div key={issueIndex} className="flex items-start space-x-2">
                              {issue.type === 'success' ? (
                                <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                              ) : (
                                <AlertCircle className="w-4 h-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                              )}
                              <span className="text-sm text-gray-600">{issue.message}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Suggestions */}
                  <div>
                    <h3 className="font-medium text-gray-900 mb-3">Key Recommendations</h3>
                    <div className="space-y-2">
                      {feedback.suggestions.map((suggestion, index) => (
                        <div key={index} className="flex items-start space-x-2">
                          <div className="w-1.5 h-1.5 bg-indigo-600 rounded-full mt-2 flex-shrink-0"></div>
                          <span className="text-sm text-gray-600">{suggestion}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;