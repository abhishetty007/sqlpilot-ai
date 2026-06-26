export default function CustomButton({
  children,
  type = "button",
  variant = "primary",
}) {
  const base =
    "w-full rounded-xl py-3 font-semibold transition-all duration-300";

  const styles = {
    primary:
      "bg-white text-black hover:bg-zinc-200 shadow-lg",
    secondary:
      "bg-zinc-800 text-white border border-zinc-700 hover:bg-zinc-700",
  };

  return (
    <button
      type={type}
      className={`${base} ${styles[variant]}`}
    >
      {children}
    </button>
  );
}