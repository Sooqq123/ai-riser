import { useState } from 'react'

function App() {
  const [searchQuery, setSearchQuery] = useState('')
  const [files, setFiles] = useState<string[]>([])
  
  // State cho cấu hình nâng cao
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [apiKey, setApiKey] = useState('')
  const [modelProvider, setModelProvider] = useState('gemini')

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <div className="w-72 bg-white border-r border-gray-200 p-4 flex flex-col overflow-y-auto">
        <h1 className="text-xl font-bold text-blue-600 mb-8">GovDoc Hub</h1>
        
        <div className="flex-1">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Kho Tài Liệu</h2>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center cursor-pointer hover:bg-gray-50 transition-colors">
            <span className="text-sm text-gray-600">Kéo thả thư mục vào đây</span>
          </div>
          
          <ul className="mt-4 space-y-2">
            {files.map((f, i) => (
              <li key={i} className="text-sm text-gray-700 bg-gray-100 p-2 rounded flex justify-between items-center">
                <span className="truncate">{f}</span>
                <button className="text-red-500 hover:text-red-700">🗑️</button>
              </li>
            ))}
          </ul>
        </div>
        
        {/* Cấu Hình Mặc Định */}
        <div className="mt-6 pt-4 border-t border-gray-200">
          <h2 className="text-sm font-semibold text-gray-500 mb-3">Chế độ hoạt động</h2>
          <label className="flex items-center space-x-2 text-sm text-gray-700 mb-2 cursor-pointer">
            <input type="radio" name="mode" className="text-blue-600" defaultChecked />
            <span>Chế độ Nhanh (Online)</span>
          </label>
          <label className="flex items-center space-x-2 text-sm text-gray-700 cursor-pointer">
            <input type="radio" name="mode" className="text-blue-600" />
            <span>Bảo mật 100% (Offline/Chậm)</span>
          </label>
        </div>

        {/* Cấu Hình Nâng Cao (BYOK) */}
        <div className="mt-4">
          <button 
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-xs text-blue-500 hover:underline w-full text-left"
          >
            {showAdvanced ? '▲ Ẩn cài đặt IT' : '▼ Cài đặt nâng cao (Dành cho IT)'}
          </button>
          
          {showAdvanced && (
            <div className="mt-3 p-3 bg-gray-50 rounded border border-gray-200 space-y-3">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Mô hình AI (Provider)</label>
                <select 
                  className="w-full text-sm p-1 border rounded"
                  value={modelProvider}
                  onChange={(e) => setModelProvider(e.target.value)}
                >
                  <option value="gemini">Google Gemini (Mặc định)</option>
                  <option value="openai">OpenAI (ChatGPT)</option>
                  <option value="anthropic">Anthropic (Claude)</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">API Key của bạn</label>
                <input 
                  type="password" 
                  className="w-full text-sm p-1 border rounded" 
                  placeholder="Nhập API Key vào đây..." 
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col p-8 items-center">
        {/* Search Bar */}
        <div className="w-full max-w-2xl mt-12 relative">
          <input 
            type="text" 
            placeholder="Tìm kiếm công văn, quyết định..." 
            className="w-full px-6 py-4 rounded-full border border-gray-300 shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-lg"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-blue-600 text-xl">
            🔍
          </button>
        </div>

        {/* Results Area */}
        <div className="w-full max-w-2xl mt-12 space-y-4">
          <div className="text-sm text-gray-500 mb-4 flex justify-between items-center">
            <span>Hiển thị 0 kết quả</span>
          </div>
          
          {/* Placeholder for empty state */}
          <div className="text-center text-gray-400 mt-20">
            <p className="text-lg">Nhập từ khóa để tìm kiếm tài liệu</p>
          </div>
        </div>
      </div>
      
      {/* Action Bar */}
      <div className="fixed bottom-0 left-72 right-0 bg-white border-t border-gray-200 p-4 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] flex justify-center space-x-4">
        <button className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-8 rounded shadow flex items-center">
          <span className="mr-2">📊</span> Trích xuất ra Excel
        </button>
        <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-8 rounded shadow flex items-center">
          <span className="mr-2">📝</span> Tổng hợp thành Báo cáo
        </button>
      </div>
    </div>
  )
}

export default App
