import React, { useState, useEffect } from 'react';
import './App.css';

function CalendarTab({ apiUrl, ideaStats, calendarStats, autopublishStatus, calendarMonth, calendarYear, setCalendarMonth, setCalendarYear, isGeneratingIdeas, setIsGeneratingIdeas, selectedDay, setSelectedDay, onRefresh }: any) {
  const [calendarData, setCalendarData] = useState<any>(null);
  const [genProgress, setGenProgress] = useState<any>(null);

  const loadCalendar = async () => {
    try {
      const r = await fetch(`${apiUrl}/api/calendar/${calendarYear}/${calendarMonth}`);
      if (r.ok) setCalendarData(await r.json());
    } catch (e) {}
  };

  useEffect(() => { loadCalendar(); }, [calendarMonth, calendarYear]);

  useEffect(() => {
    if (!isGeneratingIdeas) return;
    const iv = setInterval(async () => {
      try {
        const r = await fetch(`${apiUrl}/api/ideas/generating`);
        if (r.ok) {
          const d = await r.json();
          setGenProgress(d);
          if (!d.active) { setIsGeneratingIdeas(false); onRefresh(); }
        }
      } catch (e) {}
    }, 3000);
    return () => clearInterval(iv);
  }, [isGeneratingIdeas]);

  const handleGenerateIdeas = async () => {
    setIsGeneratingIdeas(true);
    try {
      await fetch(`${apiUrl}/api/ideas/generate`, { method: 'POST' });
    } catch (e) { setIsGeneratingIdeas(false); }
  };

  const handleToggleAutopublish = async () => {
    await fetch(`${apiUrl}/api/autopublish/toggle`, { method: 'POST' });
    onRefresh();
  };

  const prevMonth = () => {
    if (calendarMonth === 1) { setCalendarMonth(12); setCalendarYear(calendarYear - 1); }
    else setCalendarMonth(calendarMonth - 1);
  };
  const nextMonth = () => {
    if (calendarMonth === 12) { setCalendarMonth(1); setCalendarYear(calendarYear + 1); }
    else setCalendarMonth(calendarMonth + 1);
  };

  const monthName = new Date(calendarYear, calendarMonth - 1).toLocaleString('default', { month: 'long' });
  const firstDayOfWeek = new Date(calendarYear, calendarMonth - 1, 1).getDay();
  const daysInMonth = new Date(calendarYear, calendarMonth, 0).getDate();
  const today = new Date();
  const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

  const ideasAvailable = ideaStats?.available ?? 0;
  const ideasColor = ideasAvailable > 20 ? 'text-green-400' : ideasAvailable > 10 ? 'text-yellow-400' : 'text-red-400';

  const getDayEntries = (day: number) => {
    const dateStr = `${calendarYear}-${String(calendarMonth).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    return calendarData?.days?.[dateStr] || [];
  };

  return (
    <div className="space-y-6">
      {/* Stats Bar */}
      <section className="glass rounded-xl p-6">
        <div className="flex flex-wrap items-center gap-6">
          <div>
            <span className="text-white/60 text-sm">Ideas Available</span>
            <div className={`text-2xl font-bold ${ideasColor}`}>{ideasAvailable}</div>
          </div>
          <button
            onClick={handleGenerateIdeas}
            disabled={isGeneratingIdeas}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-800 disabled:opacity-50 text-white rounded-lg transition-all flex items-center gap-2"
          >
            {isGeneratingIdeas ? (
              <><div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div> Generating... {genProgress?.generated || 0}/{genProgress?.total || 100}</>
            ) : '🧠 Generate 100 Ideas'}
          </button>
          <div>
            <span className="text-white/60 text-sm">Published This Month</span>
            <div className="text-2xl font-bold text-purple-400">{calendarStats?.this_month ?? 0}</div>
          </div>
          <div>
            <span className="text-white/60 text-sm">Scheduled</span>
            <div className="text-2xl font-bold text-yellow-400">{calendarStats?.total_scheduled ?? 0}</div>
          </div>
          <div>
            <span className="text-white/60 text-sm">This Week</span>
            <div className="text-2xl font-bold text-blue-400">{calendarStats?.this_week ?? 0}</div>
          </div>
        </div>
      </section>

      {/* Calendar Grid */}
      <section className="glass rounded-xl p-6">
        <div className="flex items-center justify-between mb-6">
          <button onClick={prevMonth} className="px-3 py-1 text-white/70 hover:text-white hover:bg-white/10 rounded transition-all">&lt; Prev</button>
          <h2 className="text-xl font-bold text-white">{monthName} {calendarYear}</h2>
          <button onClick={nextMonth} className="px-3 py-1 text-white/70 hover:text-white hover:bg-white/10 rounded transition-all">Next &gt;</button>
        </div>
        <div className="grid grid-cols-7 gap-1 mb-2">
          {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(d => (
            <div key={d} className="text-center text-white/50 text-sm py-1">{d}</div>
          ))}
        </div>
        <div className="grid grid-cols-7 gap-1">
          {Array.from({ length: firstDayOfWeek }).map((_, i) => (
            <div key={`e${i}`} className="h-20 rounded bg-white/5"></div>
          ))}
          {Array.from({ length: daysInMonth }).map((_, i) => {
            const day = i + 1;
            const dateStr = `${calendarYear}-${String(calendarMonth).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            const entries = getDayEntries(day);
            const isToday = dateStr === todayStr;
            return (
              <div
                key={day}
                onClick={() => setSelectedDay(selectedDay === dateStr ? null : dateStr)}
                className={`h-20 rounded p-1 cursor-pointer transition-all hover:bg-white/15 ${
                  isToday ? 'bg-indigo-500/20 border border-indigo-400/50' : 'bg-white/5'
                } ${selectedDay === dateStr ? 'ring-2 ring-indigo-400' : ''}`}
              >
                <div className={`text-xs ${isToday ? 'text-indigo-300 font-bold' : 'text-white/60'}`}>{day}</div>
                <div className="flex flex-wrap gap-0.5 mt-1">
                  {entries.map((e: any, idx: number) => (
                    <span key={idx} className="text-xs" title={`${e.title} (${e.status})`}>
                      {e.type === 'long' ? '🔵' : e.status === 'published' ? '🟣' : e.status === 'scheduled' || e.status === 'generating' ? '🟡' : '🔴'}
                    </span>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        {/* Selected Day Details */}
        {selectedDay && (
          <div className="mt-4 p-4 bg-white/5 rounded-lg">
            <h3 className="text-white font-semibold mb-2">{selectedDay}</h3>
            {(calendarData?.days?.[selectedDay] || []).length === 0 ? (
              <p className="text-white/50 text-sm">No content this day</p>
            ) : (
              <div className="space-y-2">
                {(calendarData?.days?.[selectedDay] || []).map((e: any, i: number) => (
                  <div key={i} className="flex items-center gap-3 text-sm">
                    <span>{e.type === 'long' ? '🔵' : '🟣'}</span>
                    <span className="text-white/60">{e.time}</span>
                    <span className="text-white">{e.title}</span>
                    <span className={`px-2 py-0.5 rounded text-xs ${
                      e.status === 'published' ? 'bg-green-500/20 text-green-400' :
                      e.status === 'scheduled' ? 'bg-yellow-500/20 text-yellow-400' :
                      e.status === 'failed' ? 'bg-red-500/20 text-red-400' : 'bg-blue-500/20 text-blue-400'
                    }`}>{e.status}</span>
                    {e.youtube_url && <a href={e.youtube_url} target="_blank" rel="noreferrer" className="text-indigo-400 hover:underline">YouTube ↗</a>}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </section>

      {/* Auto-Publish Controls */}
      <section className="glass rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-white">Auto-Publish Shorts</h2>
          <button
            onClick={handleToggleAutopublish}
            className={`relative w-14 h-7 rounded-full transition-all ${
              autopublishStatus?.enabled ? 'bg-green-500' : 'bg-white/20'
            }`}
          >
            <div className={`absolute w-5 h-5 bg-white rounded-full top-1 transition-all ${
              autopublishStatus?.enabled ? 'left-8' : 'left-1'
            }`}></div>
          </button>
        </div>
        <p className="text-white/60 text-sm mb-4">2 shorts/day at 7:00 AM &amp; 9:30 PM EST</p>

        <div className="flex items-center gap-2 mb-4">
          <span className="text-white/60 text-sm">Idea Bank:</span>
          <span className={`text-sm font-semibold ${
            autopublishStatus?.idea_bank_health === 'good' ? 'text-green-400' :
            autopublishStatus?.idea_bank_health === 'low' ? 'text-yellow-400' : 'text-red-400'
          }`}>
            {autopublishStatus?.ideas_available ?? 0} ideas ({autopublishStatus?.idea_bank_health ?? 'unknown'})
          </span>
        </div>

        <h3 className="text-white/80 font-semibold mb-2 text-sm">Next 7 Publish Slots</h3>
        <div className="space-y-1">
          {(autopublishStatus?.next_slots || []).slice(0, 7).map((slot: any, i: number) => (
            <div key={i} className="flex gap-3 text-sm">
              <span className="text-white/50 w-20">{slot.day}</span>
              <span className="text-white/80">{slot.time_est}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function App() {
  const [activeTab, setActiveTab] = useState<'videos' | 'shorts' | 'calendar' | 'ceo' | 'config'>('videos');
  const [videos, setVideos] = useState<any[]>([]);
  const [jobs, setJobs] = useState<any[]>([]);
  const [health, setHealth] = useState<any>(null);
  const [videoCount, setVideoCount] = useState(5);
  const [isGenerating, setIsGenerating] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  // Shorts state
  const [shortsJobs, setShortsJobs] = useState<any[]>([]);
  const [shortsVideos, setShortsVideos] = useState<any[]>([]);
  const [shortsCount, setShortsCount] = useState(3);
  const [shortsDomain, setShortsDomain] = useState('');
  const [shortsHookCat, setShortsHookCat] = useState('');
  const [isGeneratingShorts, setIsGeneratingShorts] = useState(false);
  const [domains, setDomains] = useState<string[]>([]);
  const [hookCategories, setHookCategories] = useState<string[]>([]);
  const [hooksData, setHooksData] = useState<any>(null);
  const [showHooks, setShowHooks] = useState(false);

  // CEO state
  const [ceoStatus, setCeoStatus] = useState<any>(null);
  const [ceoLogs, setCeoLogs] = useState<any[]>([]);
  const [longformStatus, setLongformStatus] = useState<any>(null);
  const [isRunningCeoCheck, setIsRunningCeoCheck] = useState(false);

  // Calendar state
  const [calendarMonth, setCalendarMonth] = useState(new Date().getMonth() + 1);
  const [calendarYear, setCalendarYear] = useState(new Date().getFullYear());
  const [calendarData, setCalendarData] = useState<any>(null);
  const [calendarStats, setCalendarStats] = useState<any>(null);
  const [ideaStats, setIdeaStats] = useState<any>(null);
  const [isGeneratingIdeas, setIsGeneratingIdeas] = useState(false);
  const [autopublishStatus, setAutopublishStatus] = useState<any>(null);
  const [selectedDay, setSelectedDay] = useState<string | null>(null);

  const apiUrl = 'http://localhost:3011';

  const loadData = async (isInitial = false) => {
    try {
      if (isInitial) setLoading(true);

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

      // Shorts data
      try {
        const sjResp = await fetch(`${apiUrl}/api/shorts/jobs`);
        if (sjResp.ok) {
          const d = await sjResp.json();
          setShortsJobs(Array.isArray(d?.jobs) ? d.jobs : []);
        }
      } catch (e) {}

      try {
        const svResp = await fetch(`${apiUrl}/api/shorts/videos`);
        if (svResp.ok) {
          const d = await svResp.json();
          setShortsVideos(Array.isArray(d?.videos) ? d.videos : []);
        }
      } catch (e) {}

      // Domains (for dropdown)
      try {
        const dResp = await fetch(`${apiUrl}/api/domains`);
        if (dResp.ok) {
          const d = await dResp.json();
          setDomains(Object.keys(d));
        }
      } catch (e) {}

      // Hook categories
      try {
        const hResp = await fetch(`${apiUrl}/api/shorts/hooks`);
        if (hResp.ok) {
          const d = await hResp.json();
          setHookCategories(Object.keys(d?.categories || {}));
          setHooksData(d);
        }
      } catch (e) {}

      // Calendar data
      try {
        const [ideaR, calStatsR, apR] = await Promise.all([
          fetch(`${apiUrl}/api/ideas/stats`),
          fetch(`${apiUrl}/api/calendar/stats`),
          fetch(`${apiUrl}/api/autopublish/status`),
        ]);
        if (ideaR.ok) setIdeaStats(await ideaR.json());
        if (calStatsR.ok) setCalendarStats(await calStatsR.json());
        if (apR.ok) setAutopublishStatus(await apR.json());
      } catch (e) {}

      // CEO data
      try {
        const [ceoR, ceoLogsR, lfR] = await Promise.all([
          fetch(`${apiUrl}/api/ceo/status`),
          fetch(`${apiUrl}/api/ceo/logs?count=20`),
          fetch(`${apiUrl}/api/longform/status`),
        ]);
        if (ceoR.ok) setCeoStatus(await ceoR.json());
        if (ceoLogsR.ok) { const d = await ceoLogsR.json(); setCeoLogs(d.logs || []); }
        if (lfR.ok) setLongformStatus(await lfR.json());
      } catch (e) {}

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

  const handleGenerateShorts = async () => {
    if (isGeneratingShorts) return;
    try {
      setIsGeneratingShorts(true);
      setError('');
      if (shortsCount === 1) {
        const body: any = { duration: 45 };
        if (shortsDomain) body.domain = shortsDomain;
        if (shortsHookCat) body.hook_category = shortsHookCat;
        const resp = await fetch(`${apiUrl}/api/shorts/generate`, {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        });
        if (!resp.ok) throw new Error(`Failed: ${resp.status}`);
      } else {
        const resp = await fetch(`${apiUrl}/api/shorts/generate-batch`, {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ count: shortsCount }),
        });
        if (!resp.ok) throw new Error(`Failed: ${resp.status}`);
      }
      setTimeout(loadData, 1000);
    } catch (error: any) {
      setError(error.message || 'Failed to generate shorts.');
    } finally {
      setIsGeneratingShorts(false);
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
              onClick={() => setActiveTab('shorts')}
              className={`px-6 py-3 rounded-md font-medium transition-all ${
                activeTab === 'shorts' ? 'tab-active' : 'tab-inactive'
              }`}
            >
              Shorts
            </button>
            <button
              onClick={() => setActiveTab('calendar')}
              className={`px-6 py-3 rounded-md font-medium transition-all ${
                activeTab === 'calendar' ? 'tab-active' : 'tab-inactive'
              }`}
            >
              Calendar
            </button>
            <button
              onClick={() => setActiveTab('ceo')}
              className={`px-6 py-3 rounded-md font-medium transition-all ${
                activeTab === 'ceo' ? 'tab-active' : 'tab-inactive'
              }`}
            >
              CEO
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

        {/* Shorts Tab */}
        {activeTab === 'shorts' && (
          <div className="space-y-8">
            {/* Generate Shorts */}
            <section className="glass rounded-xl p-6">
              <h2 className="text-2xl font-bold mb-6 text-white">Generate Shorts</h2>
              <div className="flex flex-wrap items-end gap-4 mb-6">
                <div>
                  <label className="block text-white/80 mb-2">Count</label>
                  <input
                    type="number" min="1" max="10"
                    value={shortsCount}
                    onChange={(e) => setShortsCount(Math.max(1, Math.min(10, parseInt(e.target.value) || 1)))}
                    className="w-20 px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    disabled={isGeneratingShorts}
                  />
                </div>
                <div>
                  <label className="block text-white/80 mb-2">Domain (optional)</label>
                  <select
                    value={shortsDomain}
                    onChange={(e) => setShortsDomain(e.target.value)}
                    className="px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    disabled={isGeneratingShorts}
                  >
                    <option value="">Random</option>
                    {domains.map(d => <option key={d} value={d}>{d}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-white/80 mb-2">Hook Category (optional)</label>
                  <select
                    value={shortsHookCat}
                    onChange={(e) => setShortsHookCat(e.target.value)}
                    className="px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    disabled={isGeneratingShorts}
                  >
                    <option value="">Auto</option>
                    {hookCategories.map(c => <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>)}
                  </select>
                </div>
                <button
                  onClick={handleGenerateShorts}
                  disabled={isGeneratingShorts}
                  className="btn-primary px-8 py-2 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isGeneratingShorts ? 'Generating...' : `Generate ${shortsCount} Short${shortsCount > 1 ? 's' : ''}`}
                </button>
              </div>

              {/* Shorts Jobs */}
              {shortsJobs.length > 0 && (
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-white">Shorts Jobs ({shortsJobs.length})</h3>
                  {shortsJobs.map((job: any) => {
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
                                {job.duration}s • {job.hook_text ? `"${job.hook_text.slice(0, 50)}..."` : job.message || status}
                              </p>
                            </div>
                          </div>
                          <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold ${
                            isCompleted ? 'bg-green-500/20 text-green-400' :
                            isFailed ? 'bg-red-500/20 text-red-400' :
                            'bg-blue-500/20 text-blue-400'
                          }`}>
                            {status}
                          </span>
                        </div>
                        <div className="w-full bg-white/10 rounded-full h-2">
                          <div className="progress-bar h-2 rounded-full transition-all duration-500" style={{ width: `${progress}%` }} />
                        </div>
                        <p className="text-white/50 text-xs mt-1">{progress}% — {job.message}</p>
                      </div>
                    );
                  })}
                  <button onClick={loadData} className="btn-secondary px-4 py-2 rounded-lg text-sm font-medium">Refresh</button>
                </div>
              )}
            </section>

            {/* Completed Shorts Grid */}
            <section>
              <h2 className="text-2xl font-bold mb-6 text-white">Shorts Gallery ({shortsVideos.length})</h2>
              {shortsVideos.length === 0 ? (
                <div className="glass rounded-xl p-8 text-center">
                  <p className="text-white/60 text-lg">No shorts yet. Generate some!</p>
                </div>
              ) : (
                <div className="flex flex-wrap gap-6">
                  {shortsVideos.map((v: any) => (
                    <div key={v.id} className="glass rounded-xl p-3 card-hover" style={{ width: 200 }}>
                      <video controls className="rounded-lg bg-black/30" style={{ width: 176, height: 313 }}>
                        <source src={`${apiUrl}${v.url}`} type="video/mp4" />
                      </video>
                      <div className="mt-2 space-y-1">
                        <p className="text-white text-xs font-semibold leading-tight line-clamp-2">{v.title || v.id}</p>
                        {v.hook_text && <p className="text-indigo-300 text-xs italic line-clamp-2">"{v.hook_text}"</p>}
                        <p className="text-white/40 text-xs">{v.size_mb} MB</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>

            {/* Hook Library Browser */}
            <section className="glass rounded-xl p-6">
              <button onClick={() => setShowHooks(!showHooks)} className="flex items-center space-x-2 text-white font-bold text-lg">
                <span>{showHooks ? '▼' : '▶'}</span>
                <span>Hook Library ({hooksData?.total_hooks || 0} hooks, {hooksData?.total_closers || 0} closers)</span>
              </button>
              {showHooks && hooksData && (
                <div className="mt-4 space-y-4">
                  {Object.entries(hooksData.categories || {}).map(([cat, hooks]: [string, any]) => (
                    <div key={cat}>
                      <h4 className="text-indigo-300 font-semibold capitalize mb-2">{cat} ({hooks.length})</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-1">
                        {hooks.map((h: string, i: number) => (
                          <p key={i} className="text-white/60 text-sm">• {h}</p>
                        ))}
                      </div>
                    </div>
                  ))}
                  <div>
                    <h4 className="text-purple-300 font-semibold mb-2">Emotional Closers ({hooksData.emotional_closers?.length})</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-1">
                      {hooksData.emotional_closers?.map((c: string, i: number) => (
                        <p key={i} className="text-white/60 text-sm">• {c}</p>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </section>
          </div>
        )}

        {/* Calendar Tab */}
        {activeTab === 'calendar' && <CalendarTab
          apiUrl={apiUrl}
          ideaStats={ideaStats}
          calendarStats={calendarStats}
          autopublishStatus={autopublishStatus}
          calendarMonth={calendarMonth}
          calendarYear={calendarYear}
          setCalendarMonth={setCalendarMonth}
          setCalendarYear={setCalendarYear}
          isGeneratingIdeas={isGeneratingIdeas}
          setIsGeneratingIdeas={setIsGeneratingIdeas}
          selectedDay={selectedDay}
          setSelectedDay={setSelectedDay}
          onRefresh={() => loadData(false)}
        />}

        {/* CEO Tab */}
        {activeTab === 'ceo' && (
          <div className="space-y-6">
            {/* Overall Status Banner */}
            <section className="glass rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <span className="text-4xl">
                    {ceoStatus?.overall_status === 'healthy' ? '🟢' :
                     ceoStatus?.overall_status === 'degraded' ? '🟡' :
                     ceoStatus?.overall_status === 'critical' ? '🔴' : '⚪'}
                  </span>
                  <div>
                    <h2 className="text-2xl font-bold text-white capitalize">
                      {ceoStatus?.overall_status || 'Unknown'}
                    </h2>
                    <p className="text-white/60 text-sm">
                      Last check: {ceoStatus?.latest_check?.timestamp
                        ? new Date(ceoStatus.latest_check.timestamp).toLocaleString()
                        : 'Never'}
                    </p>
                  </div>
                </div>
                <button
                  onClick={async () => {
                    setIsRunningCeoCheck(true);
                    try {
                      await fetch(`${apiUrl}/api/ceo/check`, { method: 'POST' });
                      await loadData(false);
                    } catch (e) {}
                    setIsRunningCeoCheck(false);
                  }}
                  disabled={isRunningCeoCheck}
                  className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-800 disabled:opacity-50 text-white rounded-lg transition-all font-medium"
                >
                  {isRunningCeoCheck ? '⏳ Running...' : '🔍 Run Check Now'}
                </button>
              </div>
            </section>

            {/* System Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {/* Shorts Pipeline */}
              <div className={`glass rounded-xl p-5 border-l-4 ${
                ceoStatus?.latest_check?.checks?.shorts_publisher?.status === 'healthy' ? 'border-green-500' :
                ceoStatus?.latest_check?.checks?.shorts_publisher?.status === 'warning' ? 'border-yellow-500' : 'border-red-500'
              }`}>
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-white font-semibold">Shorts Pipeline</h3>
                  <span className={`px-2 py-1 rounded text-xs font-semibold ${
                    autopublishStatus?.enabled ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                  }`}>{autopublishStatus?.enabled ? 'ON' : 'OFF'}</span>
                </div>
                <p className="text-white/60 text-sm">Ideas: {autopublishStatus?.ideas_available ?? '?'}</p>
                <p className="text-white/60 text-sm">Health: {autopublishStatus?.idea_bank_health ?? 'unknown'}</p>
              </div>

              {/* Long-Form Pipeline */}
              <div className={`glass rounded-xl p-5 border-l-4 ${
                longformStatus?.enabled ? 'border-green-500' : 'border-yellow-500'
              }`}>
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-white font-semibold">Long-Form Pipeline</h3>
                  <button
                    onClick={async () => {
                      await fetch(`${apiUrl}/api/longform/toggle`, { method: 'POST' });
                      loadData(false);
                    }}
                    className={`px-2 py-1 rounded text-xs font-semibold ${
                      longformStatus?.enabled ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                    }`}
                  >{longformStatus?.enabled ? 'ON' : 'OFF'}</button>
                </div>
                <p className="text-white/60 text-sm">Buffer: {longformStatus?.days_of_buffer ?? '?'} days</p>
                <p className="text-white/60 text-sm">Last: {longformStatus?.last_generated
                  ? new Date(longformStatus.last_generated).toLocaleDateString() : 'Never'}</p>
              </div>

              {/* YouTube Health */}
              <div className={`glass rounded-xl p-5 border-l-4 ${
                ceoStatus?.latest_check?.checks?.youtube_token?.status === 'healthy' ? 'border-green-500' :
                ceoStatus?.latest_check?.checks?.youtube_token?.status === 'warning' ? 'border-yellow-500' : 'border-red-500'
              }`}>
                <h3 className="text-white font-semibold mb-3">YouTube Health</h3>
                <p className="text-white/60 text-sm">
                  Token: {ceoStatus?.latest_check?.checks?.youtube_token?.token_exists ? '✅ Present' : '❌ Missing'}
                </p>
                <p className="text-white/60 text-sm">
                  Valid: {ceoStatus?.latest_check?.checks?.youtube_token?.valid ? '✅' : '❌'}
                </p>
              </div>

              {/* Idea Bank */}
              <div className={`glass rounded-xl p-5 border-l-4 ${
                (ideaStats?.available ?? 0) > 20 ? 'border-green-500' :
                (ideaStats?.available ?? 0) > 10 ? 'border-yellow-500' : 'border-red-500'
              }`}>
                <h3 className="text-white font-semibold mb-3">Idea Bank</h3>
                <p className="text-2xl font-bold text-white">{ideaStats?.available ?? 0}</p>
                <p className="text-white/60 text-sm">available ideas</p>
                <div className="mt-2 w-full bg-white/10 rounded-full h-2">
                  <div className={`h-2 rounded-full ${
                    (ideaStats?.available ?? 0) > 20 ? 'bg-green-500' :
                    (ideaStats?.available ?? 0) > 10 ? 'bg-yellow-500' : 'bg-red-500'
                  }`} style={{ width: `${Math.min(100, ((ideaStats?.available ?? 0) / 100) * 100)}%` }}></div>
                </div>
              </div>

              {/* Disk Space */}
              <div className={`glass rounded-xl p-5 border-l-4 ${
                ceoStatus?.latest_check?.checks?.disk_space?.status === 'healthy' ? 'border-green-500' :
                ceoStatus?.latest_check?.checks?.disk_space?.status === 'warning' ? 'border-yellow-500' : 'border-red-500'
              }`}>
                <h3 className="text-white font-semibold mb-3">Disk Space</h3>
                <p className="text-2xl font-bold text-white">
                  {ceoStatus?.latest_check?.checks?.disk_space?.free_gb ?? '?'} GB
                </p>
                <p className="text-white/60 text-sm">free of {ceoStatus?.latest_check?.checks?.disk_space?.total_gb ?? '?'} GB</p>
              </div>

              {/* Error Rate */}
              <div className={`glass rounded-xl p-5 border-l-4 ${
                (ceoStatus?.latest_check?.checks?.failed_jobs?.failed_count ?? 0) === 0 ? 'border-green-500' : 'border-red-500'
              }`}>
                <h3 className="text-white font-semibold mb-3">Error Rate</h3>
                <p className="text-2xl font-bold text-white">
                  {ceoStatus?.latest_check?.checks?.failed_jobs?.failed_count ?? 0}
                </p>
                <p className="text-white/60 text-sm">failed jobs</p>
                <p className="text-white/60 text-sm">
                  {ceoStatus?.latest_check?.checks?.failed_jobs?.stuck_count ?? 0} stuck
                </p>
              </div>
            </div>

            {/* Alerts */}
            {(ceoStatus?.recent_alerts?.length ?? 0) > 0 && (
              <section className="glass rounded-xl p-6 border border-red-400/50 bg-red-400/5">
                <h3 className="text-red-400 font-bold mb-3">⚠️ Alerts</h3>
                <div className="space-y-2">
                  {ceoStatus.recent_alerts.map((alert: string, i: number) => (
                    <p key={i} className="text-red-300 text-sm">• {alert}</p>
                  ))}
                </div>
              </section>
            )}

            {/* Recent Actions Log */}
            <section className="glass rounded-xl p-6">
              <h3 className="text-white font-bold text-lg mb-4">Recent Actions Log</h3>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {ceoLogs.length === 0 ? (
                  <p className="text-white/50 text-sm">No health checks recorded yet</p>
                ) : (
                  [...ceoLogs].reverse().map((log: any, i: number) => (
                    <div key={i} className="flex items-start gap-3 py-2 border-b border-white/5">
                      <span className="text-xs mt-0.5">
                        {log.overall_status === 'healthy' ? '🟢' :
                         log.overall_status === 'degraded' ? '🟡' : '🔴'}
                      </span>
                      <div className="flex-1">
                        <p className="text-white/60 text-xs">
                          {new Date(log.timestamp).toLocaleString()}
                        </p>
                        {(log.actions_taken || []).map((a: string, j: number) => (
                          <p key={j} className="text-green-400 text-sm">✓ {a}</p>
                        ))}
                        {(log.alerts || []).map((a: string, j: number) => (
                          <p key={j} className="text-red-400 text-sm">⚠️ {a}</p>
                        ))}
                        {(log.actions_taken || []).length === 0 && (log.alerts || []).length === 0 && (
                          <p className="text-white/40 text-sm">All systems nominal</p>
                        )}
                      </div>
                    </div>
                  ))
                )}
              </div>
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
