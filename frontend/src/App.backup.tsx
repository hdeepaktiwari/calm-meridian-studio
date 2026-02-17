import React, { useState, useEffect, useCallback } from 'react';
import './App.css';
import { useApi } from './hooks/useApi';
import { useSSE } from './hooks/useSSE';
import type { 
  Job, 
  Video, 
  Domain, 
  MusicTrack, 
  AutomationState, 
  ApiHealth, 
  YouTubeStatus, 
  LeonardoCredits 
} from './types';

function App() {
  const [activeTab, setActiveTab] = useState<'videos' | 'config'>('videos');
  const [videos, setVideos] = useState<Video[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [domains, setDomains] = useState<Domain[]>([]);
  const [music, setMusic] = useState<MusicTrack[]>([]);
  const [automationState, setAutomationState] = useState<AutomationState | null>(null);
  const [health, setHealth] = useState<ApiHealth | null>(null);
  const [youtubeStatus, setYoutubeStatus] = useState<YouTubeStatus | null>(null);
  const [credits, setCredits] = useState<LeonardoCredits | null>(null);
  const [videoCount, setVideoCount] = useState(5);
  const [isGenerating, setIsGenerating] = useState(false);
  const [loading, setLoading] = useState(true);

  const api = useApi();

  // Load initial data
  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const [videosData, jobsData, domainsData, musicData, automationData, healthData, youtubeData] = 
        await Promise.all([
          api.getVideos().catch(() => []),
          api.getJobs().catch(() => []),
          api.getDomains().catch(() => []),
          api.getMusic().catch(() => []),
          api.getAutomationState().catch(() => null),
          api.getHealth().catch(() => null),
          api.getYouTubeStatus().catch(() => null),
        ]);

      setVideos(videosData.sort((a: Video, b: Video) => 
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      ));
      setJobs(jobsData);
      setDomains(domainsData);
      setMusic(musicData);
      setAutomationState(automationData);
      setHealth(healthData);
      setYoutubeStatus(youtubeData);
    } catch (error) {
      console.error('Failed to load initial data:', error);
    } finally {
      setLoading(false);
    }
  }, [api]);

  // SSE event handler
  const handleSSEEvent = useCallback((eventType: string, data: any) => {
    console.log('SSE Event:', eventType, data);
    
    switch (eventType) {
      case 'init':
        if (data.jobs) setJobs(data.jobs);
        break;
      
      case 'job_update':
        setJobs(prev => prev.map(job => 
          job.id === data.id ? { ...job, ...data } : job
        ));
        
        // If job completed, refresh videos
        if (data.status === 'complete') {
          api.getVideos().then(videosData => {
            setVideos(videosData.sort((a: Video, b: Video) => 
              new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
            ));
          });
        }
        break;
        
      case 'job_created':
        setJobs(prev => [...prev, data]);
        break;
        
      case 'job_deleted':
        setJobs(prev => prev.filter(job => job.id !== data.id));
        break;
        
      case 'jobs_cleared':
        setJobs([]);
        break;
    }
  }, [api]);

  // Setup SSE
  useSSE(handleSSEEvent);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // Generate videos
  const handleGenerateVideos = async () => {
    if (isGenerating || videoCount < 1 || videoCount > 50) return;
    
    try {
      setIsGenerating(true);
      await api.generateBatch(videoCount);
    } catch (error) {
      console.error('Failed to generate videos:', error);
      alert('Failed to generate videos. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  // Delete video
  const handleDeleteVideo = async (videoId: string) => {
    if (!confirm('Are you sure you want to delete this video?')) return;
    
    try {
      await api.deleteVideo(videoId);
      setVideos(prev => prev.filter(v => v.id !== videoId));
    } catch (error) {
      console.error('Failed to delete video:', error);
      alert('Failed to delete video. Please try again.');
    }
  };

  // Publish to YouTube
  const handlePublishVideo = async (videoId: string, video: Video) => {
    try {
      const publishData = {
        title: video.seo_metadata?.title || video.title,
        description: video.seo_metadata?.description || `Calm Meridian - ${video.domain}`,
        tags: video.seo_metadata?.tags || ['calm', 'meditation', 'relaxation'],
        privacy: 'public'
      };
      
      await api.publishVideo(videoId, publishData);
      alert('Video published to YouTube successfully!');
    } catch (error) {
      console.error('Failed to publish video:', error);
      alert('Failed to publish video to YouTube. Please try again.');
    }
  };

  // Check credits
  const handleCheckCredits = async () => {
    try {
      const creditsData = await api.getCredits();
      setCredits(creditsData);
    } catch (error) {
      console.error('Failed to check credits:', error);
      alert('Failed to check credits. Please try again.');
    }
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
        <header className="text-center mb-8 animate-fade-in">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent mb-2">
            Calm Meridian Studio
          </h1>
          <p className="text-white/70 text-lg">Where the World Slows Down</p>
        </header>

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
          <div className="animate-fade-in space-y-8">
            {/* Generate Videos Section */}
            <section className="glass rounded-xl p-6">
              <h2 className="text-2xl font-bold mb-6 text-white">Generate Videos</h2>
              
              <div className="flex items-center space-x-4 mb-6">
                <div>
                  <label className="block text-white/80 mb-2">Number of Videos</label>
                  <input
                    type="number"
                    min="1"
                    max="50"
                    value={videoCount}
                    onChange={(e) => setVideoCount(Math.max(1, Math.min(50, parseInt(e.target.value) || 1)))}
                    className="w-24 px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-indigo-500"
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
                  <h3 className="text-lg font-semibold text-white">Progress</h3>
                  {jobs.map((job) => (
                    <div key={job.id} className="glass-subtle rounded-lg p-4 animate-slide-in">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-3">
                          <span className="text-2xl">{job.domain_info?.icon || '🎵'}</span>
                          <div>
                            <p className="text-white font-medium">
                              {job.domain_info?.name || job.domain}
                            </p>
                            <p className="text-white/60 text-sm">
                              {job.duration} min • Created {new Date(job.created_at).toLocaleTimeString()}
                            </p>
                          </div>
                        </div>
                        <div className="text-right">
                          <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                            job.status === 'complete' ? 'bg-green-100 text-green-800' :
                            job.status === 'failed' ? 'bg-red-100 text-red-800' :
                            job.status === 'generating' ? 'bg-blue-100 text-blue-800' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
                          </span>
                        </div>
                      </div>
                      
                      <div className="w-full bg-white/10 rounded-full h-2">
                        <div 
                          className="progress-bar h-2 rounded-full"
                          style={{ width: `${job.progress}%` }}
                        ></div>
                      </div>
                      <p className="text-white/60 text-xs mt-1">{job.progress}% complete</p>
                    </div>
                  ))}
                </div>
              )}
            </section>

            {/* Video Gallery Section */}
            <section>
              <h2 className="text-2xl font-bold mb-6 text-white">Video Gallery</h2>
              
              {videos.length === 0 ? (
                <div className="glass rounded-xl p-8 text-center">
                  <p className="text-white/60 text-lg">No videos generated yet.</p>
                  <p className="text-white/40 mt-2">Generate some videos to get started!</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {videos.map((video) => (
                    <div key={video.id} className="glass rounded-xl p-4 card-hover animate-fade-in">
                      {/* Video Player */}
                      <div className="mb-4">
                        <video
                          controls
                          className="w-full aspect-video bg-black/20 rounded-lg"
                          poster={video.thumbnail_path ? `${api.apiUrl}${video.thumbnail_path}` : undefined}
                        >
                          <source src={`${api.apiUrl}${video.file_path}`} type="video/mp4" />
                          Your browser does not support the video tag.
                        </video>
                      </div>
                      
                      {/* Video Info */}
                      <div className="space-y-3">
                        <div>
                          <h3 className="text-white font-semibold text-lg leading-tight">
                            {video.seo_metadata?.title || video.title}
                          </h3>
                          <div className="flex items-center space-x-2 text-white/60 text-sm mt-1">
                            <span>{video.domain_info?.icon || '🎵'}</span>
                            <span>{video.domain_info?.name || video.domain}</span>
                            <span>•</span>
                            <span>{video.duration} min</span>
                          </div>
                        </div>
                        
                        <p className="text-white/50 text-xs">
                          Created {new Date(video.created_at).toLocaleDateString()}
                        </p>
                        
                        {/* Action Buttons */}
                        <div className="flex space-x-2 pt-2">
                          <button
                            onClick={() => handlePublishVideo(video.id, video)}
                            className="flex-1 btn-primary px-4 py-2 rounded-lg text-sm font-medium"
                          >
                            Publish to YouTube
                          </button>
                          <button
                            onClick={() => handleDeleteVideo(video.id)}
                            className="btn-danger px-4 py-2 rounded-lg text-sm font-medium"
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </div>
        )}

        {/* Config Tab */}
        {activeTab === 'config' && (
          <div className="animate-fade-in space-y-8">
            {/* API Status */}
            <section className="glass rounded-xl p-6">
              <h2 className="text-2xl font-bold mb-6 text-white">API Status</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-center space-x-3">
                  <div className={`status-indicator ${health?.openai_configured ? 'online' : 'offline'}`}></div>
                  <span className="text-white">OpenAI API</span>
                  <span className={`text-sm ${health?.openai_configured ? 'text-green-400' : 'text-red-400'}`}>
                    {health?.openai_configured ? 'Configured' : 'Not Configured'}
                  </span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className={`status-indicator ${health?.leonardo_configured ? 'online' : 'offline'}`}></div>
                  <span className="text-white">Leonardo AI API</span>
                  <span className={`text-sm ${health?.leonardo_configured ? 'text-green-400' : 'text-red-400'}`}>
                    {health?.leonardo_configured ? 'Configured' : 'Not Configured'}
                  </span>
                </div>
              </div>
            </section>

            {/* Leonardo Credits */}
            <section className="glass rounded-xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-white">Leonardo Credits</h2>
                <button
                  onClick={handleCheckCredits}
                  className="btn-secondary px-4 py-2 rounded-lg text-sm font-medium"
                >
                  Check Credits
                </button>
              </div>
              
              {credits && (
                <div className="text-white">
                  <p className="text-lg">Remaining: <span className="font-bold text-indigo-400">{credits.remaining}</span></p>
                  <p className="text-white/60">Total: {credits.total}</p>
                </div>
              )}
            </section>

            {/* Domains */}
            <section className="glass rounded-xl p-6">
              <h2 className="text-2xl font-bold mb-6 text-white">Domains ({domains.length})</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
                {domains.map((domain) => (
                  <div key={domain.id} className="glass-subtle rounded-lg p-3 text-center">
                    <div className="text-2xl mb-2">{domain.icon}</div>
                    <p className="text-white text-sm font-medium">{domain.name}</p>
                  </div>
                ))}
              </div>
            </section>

            {/* Music Library */}
            <section className="glass rounded-xl p-6">
              <h2 className="text-2xl font-bold mb-6 text-white">Music Library ({music.length} tracks)</h2>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {music.map((track) => (
                  <div key={track.id} className="glass-subtle rounded-lg p-3 flex justify-between items-center">
                    <div>
                      <p className="text-white font-medium">{track.name}</p>
                      <p className="text-white/60 text-sm">
                        {Math.floor(track.duration / 60)}:{(track.duration % 60).toString().padStart(2, '0')} • {track.mood} • {track.type}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* Automation State */}
            {automationState && (
              <section className="glass rounded-xl p-6">
                <h2 className="text-2xl font-bold mb-6 text-white">Automation State</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-center">
                  <div className="glass-subtle rounded-lg p-4">
                    <p className="text-white/60 text-sm">Next Domain</p>
                    <p className="text-white font-bold text-lg">
                      {automationState.domains[automationState.current_domain_index]?.name || 'N/A'}
                    </p>
                  </div>
                  <div className="glass-subtle rounded-lg p-4">
                    <p className="text-white/60 text-sm">Duration</p>
                    <p className="text-white font-bold text-lg">{automationState.current_duration} min</p>
                  </div>
                  <div className="glass-subtle rounded-lg p-4">
                    <p className="text-white/60 text-sm">Music Index</p>
                    <p className="text-white font-bold text-lg">{automationState.current_music_index}</p>
                  </div>
                  <div className="glass-subtle rounded-lg p-4">
                    <p className="text-white/60 text-sm">Total Generated</p>
                    <p className="text-white font-bold text-lg">{automationState.total_generated}</p>
                  </div>
                </div>
              </section>
            )}

            {/* YouTube Status */}
            <section className="glass rounded-xl p-6">
              <h2 className="text-2xl font-bold mb-6 text-white">YouTube Status</h2>
              <div className="flex items-center space-x-3">
                <div className={`status-indicator ${youtubeStatus?.connected ? 'online' : 'offline'}`}></div>
                <span className="text-white">
                  {youtubeStatus?.connected ? 'Connected' : 'Not Connected'}
                </span>
                {youtubeStatus?.channel_name && (
                  <span className="text-white/60">• {youtubeStatus.channel_name}</span>
                )}
              </div>
            </section>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;