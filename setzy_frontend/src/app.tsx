import "./app.css";

export default function App() {
  return (
    <div style="display: flex; justify-content: space-around; align-items: center; height: 100vh">
      {/* Drag and Drop file uploader */}
      <div>box 1</div>

      {/* Chat bot UI */}
      <div class="w-96 h-[500px] bg-white rounded-lg shadow-md flex flex-col">
        <div class="bg-blue-500 text-white p-3 rounded-t-lg font-semibold">Chat</div>
        <div class="flex-1 p-3 overflow-y-auto space-y-2">
          <div class="bg-gray-100 p-2 rounded-lg max-w-[80%]">Hello!</div>
          <div class="bg-blue-500 text-white p-2 rounded-lg max-w-[80%] ml-auto">Hi there</div>
        </div>
        <div class="p-3 border-t">
          <input type="text" placeholder="Type a message..." class="w-full p-2 border rounded-lg" />
        </div>
      </div>
    </div>
  );
}
