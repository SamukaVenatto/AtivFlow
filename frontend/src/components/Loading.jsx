import React from 'react';
import { BookOpen } from 'lucide-react';

const Loading = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="text-center">
        <div className="flex items-center justify-center mb-4">
          <BookOpen className="h-12 w-12 text-blue-600 animate-pulse" />
        </div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">AtivFlow</h1>
        <p className="text-gray-600">Carregando...</p>
        <div className="mt-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
        </div>
      </div>
    </div>
  );
};

export default Loading;
