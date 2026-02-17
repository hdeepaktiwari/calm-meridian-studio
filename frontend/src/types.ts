export interface Job {
  id: string;
  domain: string;
  duration: number;
  status: 'queued' | 'generating' | 'complete' | 'failed';
  progress: number;
  created_at: string;
  domain_info?: {
    name: string;
    icon: string;
  };
}

export interface Video {
  id: string;
  title: string;
  domain: string;
  duration: number;
  file_path: string;
  thumbnail_path?: string;
  created_at: string;
  seo_metadata?: {
    title: string;
    description: string;
    tags: string[];
  };
  domain_info?: {
    name: string;
    icon: string;
  };
}

export interface Domain {
  id: string;
  name: string;
  icon: string;
  description?: string;
}

export interface MusicTrack {
  id: string;
  name: string;
  duration: number;
  mood: string;
  file_path: string;
  type: 'short' | 'long';
}

export interface AutomationState {
  current_domain_index: number;
  current_duration: number;
  current_music_index: number;
  total_generated: number;
  domains: Domain[];
}

export interface ApiHealth {
  openai_configured: boolean;
  leonardo_configured: boolean;
  status: string;
}

export interface YouTubeStatus {
  connected: boolean;
  channel_name?: string;
}

export interface LeonardoCredits {
  remaining: number;
  total: number;
}

export interface SSEEvent {
  type: 'init' | 'job_update' | 'job_created' | 'job_deleted' | 'jobs_cleared';
  data: any;
}