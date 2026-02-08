import { useState, useEffect, useCallback } from 'react'

const API_URL = 'http://192.168.29.56:3011'

// ============== Types ==============

interface Job {
  job_id: string
  status: string
  progress: number
  message: string
  domain: string
  duration: number
  video_url?: string
  video_path?: string
  seo_metadata?: { title: string; description: string; hashtags: string[] }
  youtube_info?: { video_id: string; url: string; scheduled_at?: string }
  error?: string
  created_at: string
  completed_at?: string
}

interface VideoItem {
  id: string
  name: string
  url: string
  title?: string
  description?: string
  size_mb: number
  created: string
  youtube_info?: { video_id: string; url: string; scheduled_at?: string }
}

interface NextPreview {
  domain: string
  domain_icon: string
  duration: number
  duration_label: string
  music: string
  state: AutomationState
}

interface AutomationState {
  domain_index: number
  music_index: number
  duration_index: number
  total_generated: number
}

interface ConfigData {
  domain_order: string[]
  domains: Record<string, { icon: string; name: string }>
  music: { short: MusicTrack[]; long: MusicTrack[] }
  duration_cycle: number[]
  api_status: { openai: boolean; leonardo: boolean; youtube: boolean }
  automation_state: AutomationState
}

interface MusicTrack {
  id: string
  name: string
  filename: string
  duration_seconds: number
  duration_display: string
  mood: string
}

// ============== App ==============

export default function App() {
  const [page, setPage] = useState<'videos' | 'config'>('videos')

  return (
    <div style={{ minHeight: '100vh', background: '#0a0a0f', color: '#e0e0e0', fontFamily: "'Inter', sans-serif" }}>
      <header style={{ background: '#12121a', borderBottom: '1px solid #1e1e2e', padding: '16px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h1 style={{ margin: 0, fontSize: '1.4rem', background: 'linear-gradient(135deg, #60a5fa, #a78bfa)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          🎬 Calm Meridian Studio
        </h1>
        <nav style={{ display: 'flex', gap: 8 }}>
          {(['videos', 'config'] as const).map(p => (
            <button key={p} onClick={() => setPage(p)} style={{
              padding: '8px 20px', borderRadius: 8, border: 'none', cursor: 'pointer',
              background: page === p ? '#3b82f6' : '#1e1e2e', color: page === p ? '#fff' : '#888',
              fontWeight: 600, textTransform: 'capitalize', fontSize: '0.9rem',
            }}>{p}</button>
          ))}
        </nav>
      </header>
      <main style={{ maxWidth: 1200, margin: '0 auto', padding: 24 }}>
        {page === 'videos' ? <VideosPage /> : <ConfigPage />}
      </main>
    </div>
  )
}

// ============== Videos Page ==============

function VideosPage() {
  const [count, setCount] = useState(1)
  const [generating, setGenerating] = useState(false)
  const [next, setNext] = useState<NextPreview | null>(null)
  const [jobs, setJobs] = useState<Job[]>([])
  const [videos, setVideos] = useState<VideoItem[]>([])
  const [publishing, setPublishing] = useState<Record<string, boolean>>({})
  const [deleting, setDeleting] = useState<Record<string, boolean>>({})

  const fetchNext = useCallback(() => {
    fetch(`${API_URL}/api/automation/next`).then(r => r.json()).then(setNext).catch(() => {})
  }, [])

  const fetchJobs = useCallback(() => {
    fetch(`${API_URL}/api/jobs`).then(r => r.json()).then(d => setJobs(d.jobs || [])).catch(() => {})
  }, [])

  const fetchVideos = useCallback(() => {
    fetch(`${API_URL}/api/videos`).then(r => r.json()).then(d => setVideos(d.videos || [])).catch(() => {})
  }, [])

  useEffect(() => {
    fetchNext(); fetchJobs(); fetchVideos()
    const iv = setInterval(() => { fetchJobs(); fetchVideos() }, 5000)
    return () => clearInterval(iv)
  }, [fetchNext, fetchJobs, fetchVideos])

  const handleGenerate = async () => {
    setGenerating(true)
    try {
      await fetch(`${API_URL}/api/generate-batch`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ count })
      })
      fetchJobs(); fetchNext()
    } catch (e) { console.error(e) }
    setGenerating(false)
  }

  const handlePublish = async (videoId: string, title: string, description: string, tags: string[]) => {
    setPublishing(p => ({ ...p, [videoId]: true }))
    try {
      await fetch(`${API_URL}/api/publish/${videoId}`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description, tags, privacy: 'public' })
      })
      fetchVideos(); fetchJobs()
    } catch (e) { console.error(e) }
    setPublishing(p => ({ ...p, [videoId]: false }))
  }

  const handleDelete = async (videoId: string, title: string) => {
    if (!confirm(`Delete "${title}"? This permanently removes the video from storage.`)) return
    setDeleting(d => ({ ...d, [videoId]: true }))
    try {
      await fetch(`${API_URL}/api/videos/${videoId}`, { method: 'DELETE' })
      fetchVideos(); fetchJobs()
    } catch (e) { console.error(e) }
    setDeleting(d => ({ ...d, [videoId]: false }))
  }

  const cardStyle: React.CSSProperties = {
    background: '#16161f', borderRadius: 12, padding: 16, border: '1px solid #1e1e2e',
  }

  return (
    <>
      {/* Generate Section */}
      <div style={{ ...cardStyle, marginBottom: 24 }}>
        <h2 style={{ margin: '0 0 12px', fontSize: '1.1rem' }}>Generate Videos</h2>
        {next && (
          <p style={{ margin: '0 0 12px', color: '#888', fontSize: '0.9rem' }}>
            Next: {next.domain_icon} <strong>{next.domain}</strong>, {next.duration_label}, {next.music}
            {' '} <span style={{ color: '#555' }}>| #{next.state.total_generated + 1}</span>
          </p>
        )}
        <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          <input type="number" min={1} max={50} value={count} onChange={e => setCount(Number(e.target.value))}
            style={{ width: 80, padding: '8px 12px', borderRadius: 8, border: '1px solid #2a2a3a', background: '#0d0d14', color: '#fff', fontSize: '1rem' }} />
          <button onClick={handleGenerate} disabled={generating}
            style={{ padding: '10px 24px', borderRadius: 8, border: 'none', cursor: 'pointer', background: generating ? '#333' : '#3b82f6', color: '#fff', fontWeight: 600, fontSize: '0.95rem' }}>
            {generating ? '⏳ Queuing...' : `🎬 Generate ${count} Video${count > 1 ? 's' : ''}`}
          </button>
        </div>
      </div>

      {/* Active Jobs */}
      {jobs.filter(j => j.status === 'running' || j.status === 'pending').length > 0 && (
        <div style={{ marginBottom: 24 }}>
          <h3 style={{ margin: '0 0 12px', color: '#888' }}>Active Jobs</h3>
          {jobs.filter(j => j.status !== 'completed' && j.status !== 'failed').map(job => (
            <div key={job.job_id} style={{ ...cardStyle, marginBottom: 8, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <strong>{job.domain}</strong> · {Math.floor(job.duration / 60)}min
                <span style={{ color: '#888', marginLeft: 8 }}>{job.message}</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <div style={{ width: 120, height: 6, background: '#1e1e2e', borderRadius: 3, overflow: 'hidden' }}>
                  <div style={{ width: `${job.progress}%`, height: '100%', background: job.status === 'failed' ? '#ef4444' : '#3b82f6', transition: 'width 0.3s' }} />
                </div>
                <span style={{ color: '#888', fontSize: '0.85rem', minWidth: 35 }}>{job.progress}%</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Videos Grid */}
      <h3 style={{ margin: '0 0 12px', color: '#888' }}>Generated Videos ({videos.length})</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: 16 }}>
        {/* Also show completed jobs not yet in videos list */}
        {[...videos].map(video => {
          const hasYT = !!video.youtube_info
          const isPub = publishing[video.id]
          return (
            <div key={video.id} style={cardStyle}>
              <div style={{ borderRadius: 8, overflow: 'hidden', marginBottom: 12, background: '#0d0d14' }}>
                <video
                  src={`${API_URL}${video.url}`}
                  style={{ display: 'block', width: '100%', aspectRatio: '16/9', objectFit: 'cover' }}
                  controls
                  preload="metadata"
                  poster={video.thumbnail ? `${API_URL}${video.thumbnail}` : undefined}
                />
              </div>
              <h4 style={{ margin: '0 0 4px', fontSize: '0.95rem' }}>{video.title || video.name}</h4>
              <p style={{ margin: '0 0 8px', color: '#666', fontSize: '0.8rem' }}>{video.size_mb} MB · {new Date(video.created).toLocaleDateString()}</p>
              {hasYT ? (
                <a href={video.youtube_info!.url} target="_blank" rel="noopener noreferrer"
                  style={{ color: '#ef4444', fontSize: '0.85rem', textDecoration: 'none' }}>
                  ▶ YouTube {video.youtube_info!.scheduled_at ? `(scheduled ${new Date(video.youtube_info!.scheduled_at).toLocaleDateString()})` : '(published)'}
                </a>
              ) : (
                <button onClick={() => handlePublish(video.id, video.title || video.name, video.description || '', [])}
                  disabled={isPub}
                  style={{ padding: '6px 14px', borderRadius: 6, border: 'none', cursor: 'pointer', background: isPub ? '#333' : '#22c55e', color: '#fff', fontSize: '0.85rem', fontWeight: 600 }}>
                  {isPub ? '⏳ Publishing...' : '📤 Publish'}
                </button>
              )}
              <button onClick={() => handleDelete(video.id, video.title || video.name)}
                disabled={deleting[video.id]}
                style={{ padding: '6px 14px', borderRadius: 6, border: 'none', cursor: 'pointer', background: deleting[video.id] ? '#333' : '#dc2626', color: '#fff', fontSize: '0.85rem', fontWeight: 600, marginLeft: 8 }}>
                {deleting[video.id] ? '⏳ Deleting...' : '🗑️ Delete'}
              </button>
            </div>
          )
        })}
      </div>
      {videos.length === 0 && jobs.length === 0 && (
        <p style={{ textAlign: 'center', color: '#555', padding: 40 }}>No videos yet. Generate your first batch above! 🎬</p>
      )}
    </>
  )
}

// ============== Config Page ==============

function LeonardoCredits() {
  const [credits, setCredits] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const fetchCredits = async () => {
    setLoading(true)
    try {
      const r = await fetch(`${API_URL}/api/leonardo-credits`)
      setCredits(await r.json())
    } catch { setCredits({ error: 'Failed to fetch' }) }
    setLoading(false)
  }

  return (
    <div style={{ marginTop: 12 }}>
      {!credits ? (
        <button onClick={fetchCredits} disabled={loading}
          style={{ padding: '8px 16px', borderRadius: 8, border: 'none', cursor: 'pointer', background: '#7c3aed', color: '#fff', fontSize: '0.85rem', fontWeight: 600 }}>
          {loading ? '⏳ Checking...' : '🎨 Check Leonardo Credits'}
        </button>
      ) : credits.error ? (
        <span style={{ color: '#ef4444', fontSize: '0.85rem' }}>❌ {credits.error}</span>
      ) : (
        <div style={{ padding: 12, background: '#1a1a2e', borderRadius: 8, display: 'flex', gap: 24, alignItems: 'center', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.85rem', color: '#aaa' }}>🎨 Leonardo AI Credits:</span>
          <span style={{ fontSize: '1.1rem', fontWeight: 700, color: '#22c55e' }}>{credits.total?.toLocaleString()}</span>
          <span style={{ fontSize: '0.8rem', color: '#666' }}>({credits.api_subscription_tokens?.toLocaleString()} subscription + {credits.api_paid_tokens?.toLocaleString()} paid)</span>
          {credits.renewal_date && (
            <span style={{ fontSize: '0.8rem', color: '#666' }}>Renews: {new Date(credits.renewal_date).toLocaleDateString()}</span>
          )}
          <button onClick={() => setCredits(null)} style={{ padding: '4px 10px', borderRadius: 6, border: '1px solid #333', cursor: 'pointer', background: 'transparent', color: '#888', fontSize: '0.75rem' }}>✕</button>
        </div>
      )}
    </div>
  )
}

function ConfigPage() {
  const [config, setConfig] = useState<ConfigData | null>(null)
  const [resetting, setResetting] = useState(false)
  const [playingTrack, setPlayingTrack] = useState<string | null>(null)

  useEffect(() => {
    fetch(`${API_URL}/api/config`).then(r => r.json()).then(setConfig).catch(() => {})
  }, [])

  const resetState = async () => {
    setResetting(true)
    try {
      const r = await fetch(`${API_URL}/api/config`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reset_state: true })
      })
      const d = await r.json()
      setConfig(c => c ? { ...c, automation_state: d.automation_state } : c)
    } catch (e) { console.error(e) }
    setResetting(false)
  }

  const playMusic = (filename: string, id: string) => {
    if (playingTrack === id) {
      setPlayingTrack(null)
      document.querySelectorAll('audio').forEach(a => a.pause())
      return
    }
    setPlayingTrack(id)
    const audio = new Audio(`${API_URL}/music/${filename}`)
    audio.play()
    audio.onended = () => setPlayingTrack(null)
  }

  if (!config) return <p style={{ color: '#888' }}>Loading config...</p>

  const sectionStyle: React.CSSProperties = {
    background: '#16161f', borderRadius: 12, padding: 20, border: '1px solid #1e1e2e', marginBottom: 20,
  }

  return (
    <>
      {/* API Status */}
      <div style={sectionStyle}>
        <h3 style={{ margin: '0 0 12px' }}>API Status</h3>
        <div style={{ display: 'flex', gap: 16 }}>
          {Object.entries(config.api_status).map(([key, ok]) => (
            <span key={key} style={{ padding: '6px 14px', borderRadius: 8, background: ok ? '#166534' : '#7f1d1d', color: '#fff', fontSize: '0.85rem', fontWeight: 600 }}>
              {ok ? '✅' : '❌'} {key}
            </span>
          ))}
        </div>
        <LeonardoCredits />
      </div>

      {/* Automation State */}
      <div style={sectionStyle}>
        <h3 style={{ margin: '0 0 12px' }}>Automation State</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12, marginBottom: 16 }}>
          {[
            ['Domain Index', config.automation_state.domain_index],
            ['Duration Index', config.automation_state.duration_index],
            ['Music Index', config.automation_state.music_index],
            ['Total Generated', config.automation_state.total_generated],
          ].map(([label, val]) => (
            <div key={label as string} style={{ background: '#0d0d14', padding: 12, borderRadius: 8, textAlign: 'center' }}>
              <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#60a5fa' }}>{val as number}</div>
              <div style={{ fontSize: '0.75rem', color: '#666', marginTop: 4 }}>{label as string}</div>
            </div>
          ))}
        </div>
        <button onClick={resetState} disabled={resetting}
          style={{ padding: '8px 20px', borderRadius: 8, border: 'none', cursor: 'pointer', background: '#ef4444', color: '#fff', fontWeight: 600, fontSize: '0.9rem' }}>
          {resetting ? 'Resetting...' : '🔄 Reset State'}
        </button>
      </div>

      {/* Duration Cycle */}
      <div style={sectionStyle}>
        <h3 style={{ margin: '0 0 12px' }}>Duration Cycle</h3>
        <div style={{ display: 'flex', gap: 12 }}>
          {config.duration_cycle.map((d, i) => (
            <span key={i} style={{ padding: '8px 16px', borderRadius: 8, background: '#1e1e2e', fontWeight: 600 }}>
              {d / 60} min ({d}s)
              {config.automation_state.duration_index % config.duration_cycle.length === i && ' ← next'}
            </span>
          ))}
        </div>
      </div>

      {/* Domain Order */}
      <div style={sectionStyle}>
        <h3 style={{ margin: '0 0 12px' }}>Domain Order ({config.domain_order.length})</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: 8 }}>
          {config.domain_order.map((name, i) => {
            const d = config.domains[name]
            const isCurrent = config.automation_state.domain_index % config.domain_order.length === i
            return (
              <div key={name} style={{
                padding: '10px 14px', borderRadius: 8, display: 'flex', alignItems: 'center', gap: 10,
                background: isCurrent ? '#1e3a5f' : '#0d0d14', border: isCurrent ? '1px solid #3b82f6' : '1px solid transparent',
              }}>
                <span style={{ fontSize: '0.75rem', color: '#555', width: 20 }}>{i + 1}</span>
                <span style={{ fontSize: '1.2rem' }}>{d?.icon}</span>
                <span style={{ fontSize: '0.9rem' }}>{d?.name || name}</span>
                {isCurrent && <span style={{ marginLeft: 'auto', fontSize: '0.7rem', color: '#3b82f6' }}>NEXT</span>}
              </div>
            )
          })}
        </div>
      </div>

      {/* Music Library */}
      <div style={sectionStyle}>
        <h3 style={{ margin: '0 0 12px' }}>Music Library</h3>
        {(['short', 'long'] as const).map(cat => (
          <div key={cat} style={{ marginBottom: 16 }}>
            <h4 style={{ margin: '0 0 8px', color: '#888', textTransform: 'uppercase', fontSize: '0.8rem' }}>
              {cat === 'short' ? '🎵 Short (3min videos)' : '🎶 Long (5min videos)'}
            </h4>
            {config.music[cat].map(track => (
              <div key={track.id} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '8px 12px', borderRadius: 8, background: '#0d0d14', marginBottom: 4 }}>
                <button onClick={() => playMusic(track.filename, track.id)}
                  style={{ border: 'none', background: 'none', cursor: 'pointer', fontSize: '1.1rem', padding: 0 }}>
                  {playingTrack === track.id ? '⏸' : '▶️'}
                </button>
                <span style={{ flex: 1 }}>{track.name}</span>
                <span style={{ color: '#666', fontSize: '0.85rem' }}>{track.duration_display}</span>
                <span style={{ color: '#555', fontSize: '0.8rem' }}>{track.mood}</span>
              </div>
            ))}
          </div>
        ))}
      </div>
    </>
  )
}
