import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState<'videos' | 'config'>('videos');
  const [videos, setVideos] = useState<any[]>([]);
  const [jobs, setJobs] = useState<any[]>([]);
  const [health, setHealth] = useState<any>(null);
  const [videoCount, setVideoCount] = useState(5);
  const [isGenerating, setIsGenerating] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  const apiUrl = 'http://localhost:3011';

  const loadData = async (isInitial = false) => {
    try {
      if (isInitial) setLoading(true);
      // Don't setError('') on background refreshes — avoids flicker

      try {
        const healthResponse = await fetch(`${apiUrl}/health`);
        if (healthResponse.ok) setHealth(await healthResponse.json());
      } catch (e) { console.error('Health check failed:', e); }

      try {
        const videosResponse = await fetch(`${apiUrl}/api/videos`);
        if (videosResponse.ok) {
          const data = await videosResponse.json();
          const list = data?.videos ?? data;
          setVideos(Array.isArray(list) ? list : Object.values(list));
        }
      } catch (e) { console.error('Videos fetch failed:', e); }

      try {
        const jobsResponse = await fetch(`${apiUrl}/api/jobs`);
        if (jobsResponse.ok) {
          const data = await jobsResponse.json();
          let list = data?.jobs ?? data;
          if (!Array.isArray(list)) list = Object.values(list);
          setJobs(Array.isArray(list) ? list : []);
        }
      } catch (e) { console.error('Jobs fetch failed:', e); }

      if (isInitial) setError('');
    } catch (error) {
      console.error('Failed to load data:', error);
      if (isInitial) setError('Failed to load data. Check backend connection.');
    } finally {
      if (isInitial) setLoading(false);
    }
  };

  useEffect(() => {
    loadData(true);
    const interval = setInterval(() => loadData(false), 15000);
    return () => clearInterval(interval);
  }, []);

  const handleGenerateVideos = async () => {
    if (isGenerating || videoCount < 1 || videoCount > 50) return;
    try {
      setIsGenerating(true);
      setError('');
      const response = await fetch(`${apiUrl}/api/generate-batch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ count: videoCount }),
      });
      if (!response.ok) throw new Error(`Failed: ${response.status}`);
      setTimeout(loadData, 1000);
    } catch (error: any) {
      console.error('Failed to generate videos:', error);
      setError(error.message || 'Failed to generate videos.');
    } finally {
      setIsGenerating(false);
    }
  };

  const [publishingJobs, setPublishingJobs] = useState<Record<string, 'publishing' | 'published' | 'failed'>>({});

  const handlePublish = async (jobId: string) => {
    setPublishingJobs(prev => ({ ...prev, [jobId]: 'publishing' }));
    try {
      const response = await fetch(`${apiUrl}/api/publish/${jobId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      });
      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || `Publish failed: ${response.status}`);
      }
      setPublishingJobs(prev => ({ ...prev, [jobId]: 'published' }));
      loadData();
    } catch (error: any) {
      setPublishingJobs(prev => ({ ...prev, [jobId]: 'failed' }));
      alert(`Publish failed: ${error.message}`);
    }
  };

  // Map video url → job_id for publish
  const getJobForVideo = (videoUrl: string) => {
    return jobs.find(j => j.video_url === videoUrl && j.status === 'completed');
  };

  if (loading) {
    return (
      <div className="app-container flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500 mx-auto mb-4"></div>
          <p className="text-white/70">Loading Calm Meridian Studio...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent mb-2">
            Calm Meridian Studio
          </h1>
          <p className="text-white/70 text-lg">Where the World Slows Down</p>
        </header>

        {error && (
          <div className="glass rounded-lg p-4 mb-6 border border-red-400/50 bg-red-400/10">
            <p className="text-red-400">{error}</p>
          </div>
        )}

        {/* Tabs */}
        <div className="flex justify-center mb-8">
          <div className="glass rounded-lg p-1 flex space-x-1">
            <button
              onClick={() => setActiveTab('videos')}
              className={`px-6 py-3 rounded-md font-medium transition-all ${
                activeTab === 'videos' ? 'tab-active' : 'tab-inactive'
              }`}
            >
              Videos
            </button>
            <button
              onClick={() => setActiveTab('config')}
              className={`px-6 py-3 rounded-md font-medium transition-all ${
                activeTab === 'config' ? 'tab-active' : 'tab-inactive'
              }`}
            >
              Config
            </button>
          </div>
        </div>

        {/* Videos Tab */}
        {activeTab === 'videos' && (
          <div className="space-y-8">
            {/* Generate Section */}
            <section className="glass rounded-xl p-6">
              <h2 className="text-2xl font-bold mb-6 text-white">Generate Videos</h2>
              <div className="flex items-center space-x-4 mb-6">
                <div>
                  <label className="block text-white/80 mb-2">Number of Videos</label>
                  <input
                    type="number" min="1" max="50"
                    value={videoCount}
                    onChange={(e) => setVideoCount(Math.max(1, Math.min(50, parseInt(e.target.value) || 1)))}
                    className="w-24 px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    disabled={isGenerating}
                  />
                </div>
                <div className="flex-1">
                  <button
                    onClick={handleGenerateVideos}
                    disabled={isGenerating}
                    className="btn-primary px-8 py-2 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isGenerating ? 'Generating...' : 'Generate Videos'}
                  </button>
                </div>
              </div>

              {/* Jobs Progress */}
              {jobs.length > 0 && (
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-white">Jobs ({jobs.length})</h3>
                  {jobs.map((job: any) => {
                    const status = job.status || 'unknown';
                    const progress = job.progress || 0;
                    const isCompleted = status === 'completed';
                    const isFailed = status === 'failed';

                    return (
                      <div key={job.job_id} className="glass-subtle rounded-lg p-4">
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center space-x-3">
                            <span className="text-2xl">{isCompleted ? '✅' : isFailed ? '❌' : '⏳'}</span>
                            <div>
                              <p className="text-white font-medium">{job.domain || 'Unknown'}</p>
                              <p className="text-white/60 text-sm">
                                {Math.round((job.duration || 0) / 60)} min • {job.message || status}
                              </p>
                            </div>
                          </div>
                          <div className="flex items-center space-x-3">
                            <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold ${
                              isCompleted ? 'bg-green-500/20 text-green-400' :
                              isFailed ? 'bg-red-500/20 text-red-400' :
                              'bg-blue-500/20 text-blue-400'
                            }`}>
                              {status}
                            </span>
                            {isCompleted && (
                              <span className="text-green-400 text-xs">✓ Ready</span>
                            )}
                          </div>
                        </div>
                        <div className="w-full bg-white/10 rounded-full h-2">
                          <div
                            className="progress-bar h-2 rounded-full transition-all duration-500"
                            style={{ width: `${progress}%` }}
                          />
                        </div>
                        <p className="text-white/50 text-xs mt-1">{progress}%</p>
                      </div>
                    );
                  })}
                  <button onClick={loadData} className="btn-secondary px-4 py-2 rounded-lg text-sm font-medium">
                    Refresh
                  </button>
                </div>
              )}
            </section>

            {/* Video Gallery */}
            <section>
              <h2 className="text-2xl font-bold mb-6 text-white">Video Gallery ({videos.length} videos)</h2>
              {videos.length === 0 ? (
                <div className="glass rounded-xl p-8 text-center">
                  <p className="text-white/60 text-lg">No videos yet. Generate some!</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {videos.map((video: any) => {
                    const matchedJob = getJobForVideo(video.url);
                    return (
                      <div key={video.id} className="glass rounded-xl p-4 card-hover">
                        <div className="mb-4">
                          <video
                            controls
                            className="w-full aspect-video bg-black/30 rounded-lg"
                          >
                            <source src={`${apiUrl}${video.url}`} type="video/mp4" />
                          </video>
                        </div>
                        <div className="space-y-2">
                          <h3 className="text-white font-semibold leading-tight">{video.title || video.name}</h3>
                          <p className="text-white/50 text-sm">{video.size_mb ? `${video.size_mb} MB` : ''} • {video.created ? new Date(video.created).toLocaleDateString() : ''}</p>
                          {video.description && (
                            <p className="text-white/40 text-xs line-clamp-2">{video.description}</p>
                          )}
                          <div className="pt-2">
                            {matchedJob ? (() => {
                              const isPublished = matchedJob.youtube_info || publishingJobs[matchedJob.job_id] === 'published';
                              const isPublishing = publishingJobs[matchedJob.job_id] === 'publishing';
                              const isFailed = publishingJobs[matchedJob.job_id] === 'failed';
                              return isPublished ? (
                                <button disabled className="w-full px-4 py-2 bg-green-700 text-white rounded-lg font-medium flex items-center justify-center space-x-2 cursor-default opacity-90">
                                  <span>✓</span><span>Published</span>
                                </button>
                              ) : isPublishing ? (
                                <button disabled className="w-full px-4 py-2 bg-yellow-600 text-white rounded-lg font-medium flex items-center justify-center space-x-2 cursor-wait animate-pulse">
                                  <span>⏳</span><span>Publishing...</span>
                                </button>
                              ) : (
                                <button
                                  onClick={() => handlePublish(matchedJob.job_id)}
                                  className={`w-full px-4 py-2 ${isFailed ? 'bg-red-800 hover:bg-red-700' : 'bg-red-600 hover:bg-red-700'} text-white rounded-lg font-medium transition-colors flex items-center justify-center space-x-2`}
                                >
                                  <span>▶</span><span>{isFailed ? 'Retry Publish' : 'Publish to YouTube'}</span>
                                </button>
                              );
                            })() : (
                              <span className="text-white/30 text-xs">No matching job found</span>
                            )}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </section>
          </div>
        )}

        {/* Config Tab */}
        {activeTab === 'config' && (
          <div className="space-y-8">
            <section className="glass rounded-xl p-6">
              <h2 className="text-2xl font-bold mb-6 text-white">API Status</h2>
              {health ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="flex items-center space-x-3">
                    <div className={`status-indicator ${health.api_keys?.openai ? 'online' : 'offline'}`}></div>
                    <span className="text-white">OpenAI API</span>
                    <span className={`text-sm ${health.api_keys?.openai ? 'text-green-400' : 'text-red-400'}`}>
                      {health.api_keys?.openai ? 'Configured' : 'Not Configured'}
                    </span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className={`status-indicator ${health.api_keys?.leonardo ? 'online' : 'offline'}`}></div>
                    <span className="text-white">Leonardo AI</span>
                    <span className={`text-sm ${health.api_keys?.leonardo ? 'text-green-400' : 'text-red-400'}`}>
                      {health.api_keys?.leonardo ? 'Configured' : 'Not Configured'}
                    </span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className={`status-indicator ${health.youtube_connected ? 'online' : 'offline'}`}></div>
                    <span className="text-white">YouTube</span>
                    <span className={`text-sm ${health.youtube_connected ? 'text-green-400' : 'text-red-400'}`}>
                      {health.youtube_connected ? 'Connected' : 'Not Connected'}
                    </span>
                  </div>
                </div>
              ) : (
                <p className="text-white/60">Unable to check API status</p>
              )}
            </section>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
