const getApiUrl = (): string => {
  if (import.meta.env.VITE_API_URL) return import.meta.env.VITE_API_URL;
  if (typeof window !== 'undefined') {
    const { protocol, hostname } = window.location;
    return `${protocol}//${hostname}:3011`;
  }
  return 'http://localhost:3011';
};

export const useApi = () => {
  const apiUrl = getApiUrl();

  const apiCall = async (endpoint: string, options: RequestInit = {}) => {
    try {
      const url = `${apiUrl}${endpoint}`;
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return response.json();
    } catch (error) {
      console.error('API call failed:', error);
      throw error;
    }
  };

  const generateBatch = async (count: number) => {
    return apiCall('/api/generate-batch', {
      method: 'POST',
      body: JSON.stringify({ count }),
    });
  };

  const getJobs = async () => {
    return apiCall('/api/jobs');
  };

  const getVideos = async () => {
    return apiCall('/api/videos');
  };

  const deleteVideo = async (videoId: string) => {
    return apiCall(`/api/videos/${videoId}`, {
      method: 'DELETE',
    });
  };

  const publishVideo = async (videoId: string, publishData: any) => {
    return apiCall(`/api/publish/${videoId}`, {
      method: 'POST',
      body: JSON.stringify(publishData),
    });
  };

  const getDomains = async () => {
    return apiCall('/api/domains');
  };

  const getMusic = async () => {
    return apiCall('/api/music');
  };

  const getCredits = async () => {
    return apiCall('/api/credits');
  };

  const getAutomationState = async () => {
    return apiCall('/api/automation-state');
  };

  const getYouTubeStatus = async () => {
    return apiCall('/api/youtube/status');
  };

  const getHealth = async () => {
    return apiCall('/health');
  };

  return {
    generateBatch,
    getJobs,
    getVideos,
    deleteVideo,
    publishVideo,
    getDomains,
    getMusic,
    getCredits,
    getAutomationState,
    getYouTubeStatus,
    getHealth,
    apiUrl,
  };
};