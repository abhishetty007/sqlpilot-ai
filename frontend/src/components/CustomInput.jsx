export default function CustomInput({
  type = "text",
  placeholder,
  value,
  onChange,
}) {
  return (
    <input
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className="
        w-full
        rounded-xl
        border
        border-zinc-700
        bg-zinc-900
        px-4
        py-3
        text-white
        placeholder:text-zinc-500
        outline-none
        transition-all
        duration-300
        focus:border-blue-500
        focus:ring-2
        focus:ring-blue-500/30
      "
    />
  );
}